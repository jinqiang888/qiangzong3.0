FROM node:22-bookworm

# Create OpenClaw-compatible directory structure
RUN mkdir -p /home/node/.openclaw/agents/main/sessions \
    && mkdir -p /workspace/skills/evolver/memory

# Working directory matches OpenClaw convention
WORKDIR /workspace/skills/evolver

# Copy the evolver skill (build output)
COPY dist-public/ /workspace/skills/evolver/

# Copy test infrastructure
COPY test/fixtures/ /workspace/skills/evolver/test/fixtures/
COPY test/vibe_test.js /workspace/skills/evolver/test/vibe_test.js
COPY test/llm_helper.js /workspace/skills/evolver/test/llm_helper.js

# Place mock session log where evolve.js expects it
COPY test/fixtures/session_mock.jsonl /home/node/.openclaw/agents/main/sessions/mock_session.jsonl

# Initialize a git repo so solidify's git commands work.
# Must happen before chown, and we mark directory as safe for all users.
RUN cd /workspace/skills/evolver \
    && git init \
    && git config --global --add safe.directory /workspace/skills/evolver \
    && git config user.email "vibe-test@local" \
    && git config user.name "vibe-test" \
    && git add -A \
    && git commit -m "init" --quiet

# Ensure node user owns everything and can use git
RUN chown -R node:node /workspace /home/node/.openclaw /workspace/skills/evolver/.git

USER node

# Mark safe directory for node user too
RUN git config --global --add safe.directory /workspace/skills/evolver

ENV AGENT_NAME=main
ENV EVOLVE_BRIDGE=false
ENV HOME=/home/node
ENV NODE_ENV=test

CMD ["node", "test/vibe_test.js"]
