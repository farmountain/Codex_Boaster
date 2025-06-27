# Technical Solution

The system follows a TDD-first workflow guided by six cooperating agents:

1. **ArchitectAgent** breaks a user goal into modules and logs the plan to
   HipCortex.
2. **BuilderAgent** generates minimal code to satisfy the tests.
3. **TesterAgent** runs pytest on the generated code.
4. **ReflexionAgent** applies the AUREUS reasoning loop to failed test output and
   updates the BuilderAgent instructions.
5. **ExporterAgent** packages artefacts once tests pass.
6. **MonetizerAgent** records usage and creates Stripe charges.

All memory and reasoning context flows through `hipcortex_bridge.py`.  The
`build_test_cycle` function encapsulates the round‑trip from code generation to
testing and reflexion.

The frontend polls `/test_results` and `/improvement_suggestion` to provide live
feedback during the build process.
