use std::{collections::HashMap, error::Error, fs, path::PathBuf};

use dirs::home_dir;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Default)]
pub struct CredentialStore {
    providers: HashMap<String, String>,
}

impl CredentialStore {
    fn path() -> Result<PathBuf, Box<dyn Error>> {
        let mut dir = home_dir().ok_or("home dir not found")?;
        dir.push(".boaster");
        fs::create_dir_all(&dir)?;
        dir.push("credentials.json");
        Ok(dir)
    }

    pub fn load() -> Result<Self, Box<dyn Error>> {
        let path = Self::path()?;
        if path.exists() {
            let data = fs::read_to_string(path)?;
            Ok(serde_json::from_str(&data)?)
        } else {
            Ok(Self::default())
        }
    }

    pub fn save(&self) -> Result<(), Box<dyn Error>> {
        let path = Self::path()?;
        let data = serde_json::to_string_pretty(self)?;
        fs::write(path, data)?;
        Ok(())
    }

    pub fn get(&self, provider: &str) -> Option<String> {
        self.providers.get(provider).cloned()
    }

    pub fn set(&mut self, provider: &str, key: String) {
        self.providers.insert(provider.to_string(), key);
    }
}

pub fn load_env() {
    let _ = dotenvy::from_filename(".env.local");
}
