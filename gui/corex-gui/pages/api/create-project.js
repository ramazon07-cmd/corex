import { exec } from 'child_process';
import { promisify } from 'util';

const execPromise = promisify(exec);

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { projectName, auth, ui, database, docker, api } = req.body;

  // Validate inputs
  if (!projectName) {
    return res.status(400).json({ error: 'Project name is required' });
  }

  try {
    // Construct the CoreX command
    let command = `corex new ${projectName}`;
    
    if (auth) command += ` --auth=${auth}`;
    if (ui) command += ` --ui=${ui}`;
    if (database) command += ` --database=${database}`;
    if (docker) command += ' --docker';
    if (api) command += ' --api';

    // Execute the command
    const { stdout, stderr } = await execPromise(command, { cwd: process.env.HOME });
    
    return res.status(200).json({
      success: true,
      message: `Project '${projectName}' created successfully!`,
      command,
      output: stdout,
      error: stderr
    });
  } catch (error) {
    return res.status(500).json({
      success: false,
      message: 'Failed to create project',
      error: error.message
    });
  }
}