// deploy-local.js
import { FreestyleSandboxes } from "freestyle-sandboxes";
import { prepareDirForDeploymentSync } from "freestyle-sandboxes/utils";
import dotenv from 'dotenv';

dotenv.config();

const api = new FreestyleSandboxes({
  apiKey: process.env.FREESTYLE_API_KEY,
});

async function deployLocal() {
  try {
    // This prepares your local directory for deployment
    const localFiles = prepareDirForDeploymentSync("./crypto-ai-agent"); // Path to your Next.js app
    
    const result = await api.deployWeb(
      localFiles,  // Your local files
      {
        domains: ["crypto-ai-agent.style.dev"],
        build: true,  // Let Freestyle build your Next.js app
      }
    );
    
    console.log("Successfully deployed local app!");
    console.log("Available at:", result.domains);
  } catch (error) {
    console.error("Deployment failed:", error);
  }
}

deployLocal();

