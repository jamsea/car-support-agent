# car-support-agent

A Pipecat AI voice agent built with a cascade pipeline (STT → LLM → TTS).

## Configuration

- **Bot Type**: Web
- **Transport(s)**: Daily (WebRTC), SmallWebRTC
- **Pipeline**: Cascade
  - **STT**: Deepgram Nova-3, Australian English (`en-AU`)
  - **LLM**: OpenAI
  - **TTS**: Deepgram Aura-2, Australian voice (`aura-2-theia-en`)
- **Turn detection**: Pipecat defaults (Silero VAD + local smart-turn)
- **Conversation**: a 4-node Pipecat Flow in `server/flow.py`
- **Features**:
  - Transcription
  - Krisp Noise Cancellation

## Setup

### Server

1. **Navigate to server directory**:

   ```bash
   cd server
   ```

2. **Install dependencies**:

   ```bash
   uv sync
   ```

3. **Configure environment variables**:

   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

4. **Run the bot**:

   - Daily: `uv run bot.py --transport daily`
   - SmallWebRTC: `uv run bot.py`

### Evals

The audio evals play a caller against the running bot and check each step of the
front desk flow. They use cloud services only: Deepgram for the caller's voice and
for transcribing the bot, and OpenAI as the judge.

1. Start the bot in one terminal: `uv run bot.py`
2. Run the evals in another:

   ```bash
   uv run python -m pipecat.evals run evals/front_desk.yaml -v -a \
     --record-dir eval-runs/recordings --logs-dir eval-runs/logs
   ```

Recordings land in `server/eval-runs/recordings/`.

### Client

1. **Navigate to client directory**:

   ```bash
   cd client
   ```

2. **Install dependencies**:

   ```bash
   npm install
   ```

3. **Configure environment variables**:

   ```bash
   cp env.example .env.local
   # Edit .env.local if needed (defaults to localhost:7860)
   ```

   > **Note:** Environment variables in Vite are bundled into the client and exposed in the browser. For production applications that require secret protection, consider implementing a backend proxy server to handle API requests and manage sensitive credentials securely.

4. **Run development server**:

   ```bash
   npm run dev
   ```

5. **Open browser**:

   http://localhost:5173

## Project Structure

```
car-support-agent/
├── server/              # Python bot server
│   ├── bot.py           # Main bot implementation
│   ├── flow.py          # Front desk conversation flow
│   ├── evals/           # Audio eval scenarios and their cloud services
│   ├── pyproject.toml   # Python dependencies
│   ├── env.example      # Environment variables template
│   ├── .env             # Your API keys (git-ignored)
│   └── pcc-deploy.toml  # Pipecat Cloud deployment config
├── client/              # React application
│   ├── src/             # Client source code
│   ├── package.json     # Node dependencies
│   └── ...
├── Dockerfile           # Container image for Pipecat Cloud (built from the repo root)
├── .gitignore           # Git ignore patterns
└── README.md            # This file
```

## Sharing a demo

`client/` can be hosted on GitHub Pages and pointed at the agent on Pipecat Cloud.
`.github/workflows/pages.yml` builds and deploys it on every push to `main` that
touches `client/`.

One-time setup:

1. Deploy the agent to Pipecat Cloud (see below).
2. Push this repo to GitHub and turn on Pages (Settings > Pages > Source: GitHub Actions).
3. If the repo is not named `car-support-agent`, change `base` in `client/vite.config.ts`.

The page then lives at `https://<your-user>.github.io/car-support-agent/`. Paste a
Pipecat Cloud public key (`pk_...`) into the box at the top and click Connect. Make
a key in the Pipecat Cloud dashboard under Settings > API Keys > Public.

To share it, put the key in the link. The page fills the box for you:

```
https://<your-user>.github.io/car-support-agent/#key=pk_...
```

Anyone with that link can start calls on your account. Make one key per person,
and revoke it when they are done.

Add `?agent=<name>` to the link if your agent has another name. `npm run dev`
still talks to the local bot and shows no key box.

## Deploying to Pipecat Cloud

This project is configured for deployment to Pipecat Cloud. You can learn how to deploy to Pipecat Cloud in the [Pipecat Quickstart Guide](https://docs.pipecat.ai/getting-started/quickstart#step-2-deploy-to-production).

Refer to the [Pipecat Cloud Documentation](https://docs.pipecat.ai/deployment/pipecat-cloud/introduction) to learn more about configuring, deploying, and managing your agents in Pipecat Cloud.

## Learn More

- [Pipecat Documentation](https://docs.pipecat.ai/)
- [Voice UI Kit Documentation](https://voiceuikit.pipecat.ai/)
- [Pipecat GitHub](https://github.com/pipecat-ai/pipecat)
- [Pipecat Examples](https://github.com/pipecat-ai/pipecat-examples)
- [Discord Community](https://discord.gg/pipecat)