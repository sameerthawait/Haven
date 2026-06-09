# Running Haven in Your Workspace

Welcome to **Haven**, a self-hosted, local-first AI workspace. Haven is designed to run securely on your own hardware, keeping your chats, documents, email, calendar, and notes completely private.

This guide explains how to set up and run Haven for yourself, and how to securely share it with others in a local network or team environment.

---

## Quick Start

### 1. Docker (Recommended)
Docker runs Haven and its bundle of supporting services (ntfy, ChromaDB, and SearXNG) in an isolated network environment.

```bash
# Clone the repository
git clone <repository-url>
cd haven

# Copy environment template
cp .env.example .env

# Build and start services in the background
docker compose up -d --build
```
Once healthy, open `http://localhost:7000` in your browser. Log in using the admin password printed in the startup logs (`docker compose logs haven`).

### 2. Native Windows
Run the automated launcher script to set up a virtual environment, install dependencies, and run the FastAPI server:

```powershell
# Run the PowerShell launcher
powershell -ExecutionPolicy Bypass -File .\launch-windows.ps1
```
Open `http://127.0.0.1:7000` to access the Haven UI.

### 3. Native macOS / Linux
Use the macOS launcher to set up homebrew dependencies and accelerate model serving using Metal:

```bash
# Start macOS setup and server
./start-macos.sh
```
Open `http://127.0.0.1:7860` (or the custom port printed by the script).

---

## Sharing Haven in a Local Network or Team Workspace

To allow other people in your organization or home network to access your Haven instance, follow these steps:

### 1. Bind to Network Interfaces
By default, Haven binds only to `127.0.0.1` (localhost) for security. To expose it to your local area network (LAN) or a VPN (like Tailscale):

*   **Docker Compose**: Set `APP_BIND=0.0.0.0` in your `.env` file.
*   **Native Windows/macOS**: Set the environment variable `HAVEN_HOST=0.0.0.0` before running the server, or edit your launch variables.

> [!WARNING]
> Binding to `0.0.0.0` allows anyone on your network to reach the port. Ensure your firewall blocks public traffic to this port, or use a secure VPN.

### 2. Set Up a Secure VPN (Tailscale / WireGuard)
Instead of opening firewall ports on your router, have users install **Tailscale**.
1. Install Tailscale on the host machine running Haven.
2. Install Tailscale on the devices of other users.
3. Users can then access the workspace using the host's Tailscale IP (e.g. `http://100.x.y.z:7000`).

### 3. Secure with HTTPS (Caddy / Nginx Reverse Proxy)
Browsers disable certain secure features (like voice recording/microphone access and local storage capabilities) on non-localhost HTTP connections. If you share Haven over the network, **you must use HTTPS**.

Using **Caddy** is the simplest way to get automated HTTPS for local networks:

1. Install Caddy on the host machine.
2. Create a `Caddyfile` in the project directory:
   ```caddy
   # Expose using a Tailscale hostname or local IP
   my-haven-host.tailscale-net:443 {
       reverse_proxy 127.0.0.1:7000
   }
   ```
3. Run `caddy run`. Other users can now connect securely at `https://my-haven-host.tailscale-net`.

### 4. Enable Authentication & Secure Cookies
For any network-exposed deployment, ensure these configurations are set in your `.env` file:
```bash
# Enforce login screen
AUTH_ENABLED=true

# Disable development-only localhost bypass
LOCALHOST_BYPASS=false

# Enforce secure cookies (only set if serving over HTTPS)
SECURE_COOKIES=true
```

### 5. Multi-User & Member Privileges
Haven supports multi-user separation of data. Each user gets their own inbox, calendar, document library, notes, and memory database.

*   On first boot, the first account created is the **Admin**.
*   Admins can configure global settings, local served models, and MCP servers.
*   Standard users have access only to their own data. Review privileges under **Settings → Admin Controls** to manage what standard users can do (e.g., restricting image generation or preventing shell tool execution).
