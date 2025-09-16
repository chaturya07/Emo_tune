# Spotify Developer Setup

## 1. Chosen API & Auth Flow
We are using **Spotify Web API** with **Authorization Code Flow (with Refresh Tokens)**.  

### Why This Flow?
- Access **user-level data**: playlists, liked songs, playback.
- Allows **full-track playback** after login.
- **Refresh tokens** prevent repeated logins.
- **More secure** than Implicit Grant.

---

## 2. Steps to Obtain Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. Click **Create an App**.
3. Copy **Client ID** and **Client Secret**.
4. Add Redirect URIs in the app settings:
   - **Local Development:** `http://localhost:8888/callback`
   - **Deployed App:** `https://yourapp.com/callback`
5. Save changes and paste credentials into your local `.env` file (see section 3).

---

## 3. Environment Variables

Create a `.env` file at the **project root** (not inside `venv/`):

```env
# Spotify API credentials
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here

# Redirect URI (must match exactly what you set in the Spotify Dashboard)
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
**Important:**

- Commit `.env.example` to GitHub.
- Add `.env` to `.gitignore` to avoid leaking secrets.

---

## 4. Token Handling

- Exchange authorization code for:
  - **Access Token** (short-lived)
  - **Refresh Token** (long-lived)
- Store tokens securely (never commit to GitHub).
- Use refresh token to generate new access tokens automatically.

---

## 5. Secret Rotation

If your Client Secret is ever exposed:

1. Go to **Spotify Developer Dashboard → Your App**.
2. Click **Regenerate Secret**.
3. Update the `.env` file with the new secret.
4. Restart backend or redeploy your app.

---

## 6. Required Scopes

We will request the following Spotify scopes:

- `user-read-private`
- `user-read-email`
- `playlist-read-private`
- `playlist-modify-private`
- `user-library-read`
- `user-modify-playback-state`
- `user-read-playback-state`
