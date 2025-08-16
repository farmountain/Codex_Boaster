use clap::{Parser, Subcommand};
use futures_util::{SinkExt, StreamExt};
use reqwest::Client;
use serde_json::{json, Value};
use tokio_tungstenite::connect_async;
use tokio_tungstenite::tungstenite::Message;

mod credentials;
use credentials::{load_env, CredentialStore};

#[derive(Parser)]
#[command(name = "boaster")]
#[command(about = "CLI for Codex Boaster", long_about = None)]
struct Cli {
    /// Base URL for the Boaster API
    #[arg(long, default_value = "http://localhost:8000")]
    api_url: String,

    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Initialise a new project in Boaster
    Init { project: String },
    /// Request a plan from Boaster
    Plan { project: String },
    /// Run the current project and stream output to Goose
    Run {
        project: String,
        #[arg(long, default_value = "ws://localhost:9001/run")]
        ws_url: String,
    },
    /// Evaluate the project
    Eval { project: String },
    /// Deploy the project
    Deploy { project: String },
    /// List available MCP tools
    Tools,
    /// Manage stored API credentials
    Creds {
        #[command(subcommand)]
        action: CredAction,
    },
}

#[derive(Subcommand)]
enum CredAction {
    /// Store a provider API key
    Set { provider: String, key: String },
    /// Retrieve a provider API key
    Get { provider: String },
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    load_env();
    let cli = Cli::parse();
    let client = Client::new();

    match cli.command {
        Commands::Init { project } => {
            let res = client
                .post(format!("{}/init", cli.api_url))
                .json(&json!({"project": project}))
                .send()
                .await?;
            println!("{}", res.text().await?);
        }
        Commands::Plan { project } => {
            let res = client
                .post(format!("{}/plan", cli.api_url))
                .json(&json!({"project": project}))
                .send()
                .await?;
            println!("{}", res.text().await?);
        }
        Commands::Run { project, ws_url } => {
            let res = client
                .post(format!("{}/run", cli.api_url))
                .json(&json!({"project": project}))
                .send()
                .await?;
            println!("Run started: {}", res.text().await?);

            let (mut ws_stream, _) = connect_async(ws_url).await?;
            ws_stream.send(Message::Text("start".into())).await?;
            while let Some(msg) = ws_stream.next().await {
                let msg = msg?;
                if msg.is_text() {
                    println!("{}", msg.into_text()?);
                }
            }
        }
        Commands::Eval { project } => {
            let res = client
                .post(format!("{}/eval", cli.api_url))
                .json(&json!({"project": project}))
                .send()
                .await?;
            println!("{}", res.text().await?);
        }
        Commands::Deploy { project } => {
            let res = client
                .post(format!("{}/deploy", cli.api_url))
                .json(&json!({"project": project}))
                .send()
                .await?;
            println!("{}", res.text().await?);
        }
        Commands::Tools => {
            let schemas: Value = serde_json::from_str(include_str!("../../shared/tool_schemas.json"))?;
            println!("{}", serde_json::to_string_pretty(&schemas)?);
        }
        Commands::Creds { action } => {
            let mut store = CredentialStore::load()?;
            match action {
                CredAction::Set { provider, key } => {
                    store.set(&provider, key);
                    store.save()?;
                    println!("stored {}", provider);
                }
                CredAction::Get { provider } => {
                    if let Some(k) = store.get(&provider) {
                        println!("{}", k);
                    } else {
                        eprintln!("no key for {}", provider);
                    }
                }
            }
        }
    }

    Ok(())
}
