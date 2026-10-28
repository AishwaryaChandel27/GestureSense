# GestureSense — Webcam Hand Gestures

A Flask webcam demo that uses MediaPipe hand landmarks and geometric rules to recognize four static gestures, displaying annotated frames in a browser.

## What it implements

- Recognize open palm, fist, peace sign and thumbs up.
- Overlay hand landmarks, bounding boxes and gesture labels.
- Start or stop the server’s camera through the web interface.
- Read the latest gesture as JSON.

## How it works

`CameraHandler` captures frames on the machine running Flask. `GestureRecognizer` runs MediaPipe Hands for one hand, then applies finger-position rules. Flask serves multipart JPEG frames through `/video_feed` and JSON through `/gesture_info`.

## Current limitations

This is the server’s webcam, not a remote browser camera. The stream stops after at most 100 frames per request. Confidence values such as 0.9 are fixed rule outputs, not calibrated model probabilities. Thumb logic depends on orientation. Camera-control routes have no authentication in the reviewed code.

## Run locally

The commands below were checked against source paths and manifests; application startup was not tested unless explicitly stated.
Python 3.11 or newer is declared in `pyproject.toml`. Use uv for the checked-in project/lockfile. Set environment variables in the shell or process manager; the Python entry points do not explicitly load `.env`.

```bash
git clone --branch main https://github.com/AishwaryaChandel27/GestureSense.git
cd GestureSense
uv sync
uv run python main.py
```
Open `http://localhost:5000`. 

## Configuration

| Variable | Purpose / requirement |
| --- | --- |
| `SESSION_SECRET` | Set a private random value; code otherwise uses a development fallback |

Use your own credentials. Never commit populated secret values.

## Usage

Run on a computer with an accessible webcam, open the page, start the camera and hold one gesture in view. Refresh or reconnect when the finite frame stream ends.

### API example

```bash
curl http://localhost:5000/gesture_info
```

The response contains `gesture` and `confidence`. `GET /start_camera` returns a `success` boolean; `GET /stop_camera` stops the shared capture device.

## Source map

| Path | Responsibility |
| --- | --- |
| [app.py](app.py) | Flask routes and finite video stream |
| [camera_handler.py](camera_handler.py) | OpenCV camera lifecycle |
| [gesture_recognizer.py](gesture_recognizer.py) | MediaPipe and gesture rules |
| [static/js/main.js](static/js/main.js) | Browser controls |
| [templates/index.html](templates/index.html) | UI |

## Validation

Documentation was checked against the repository snapshot on 28 October 2026. No application test suite was run for this repository. Provider availability, browser behavior, builds and deployment are unverified.

## Demo capture

Suggested addition: a short recording of the usage workflow above, with synthetic inputs and visible limitations. No new screenshot or recording was produced in this audit.

## Contributing

Open an issue with reproduction steps or submit a focused pull request. Keep prototype behavior and future plans clearly distinguished, and include verification steps for changes.

## License

No license file was found. A manifest or older README license label does not replace an explicit license grant.

Maintained in [AishwaryaChandel27’s repositories](https://github.com/AishwaryaChandel27).
