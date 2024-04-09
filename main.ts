import { Octokit } from "@octokit/rest";
import { config } from 'dotenv';

config();

let octokit: Octokit = new Octokit({auth: process.env.GITHUB_TOKEN});

async function fetchIssues() {
  const response = await octokit.rest.issues.listForAuthenticatedUser({
    filter: 'assigned',
    state: 'open',
  });

  console.dir(response.data);
}

fetchIssues().then(() => {
  console.log('Done');
})
