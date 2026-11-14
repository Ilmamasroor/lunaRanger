"""Authoritative Mission REST API Server for the TypeScript Simulation Engine.

Provides CORS-enabled endpoints:
- GET /api/mission-config       -> Validated Schema 1.1 parameters (outputs/mission_config.json)
- GET /api/scenarios/emergency  -> Space weather emergency scenarios (from NASA DONKI)
- GET /api/fixtures/life-support-> Life support mass-balance expected calculations for TS engine tests
- GET /api/fixtures/radiation   -> Radiation dose calculation fixtures for TS engine tests
- GET /api/health               -> Pipeline status & timestamps
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent

class MissionAPIHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        # Enable CORS for React/Vite/Next.js/WebGL frontends
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        # Normalize path
        path = self.path.split("?")[0].rstrip("/")
        
        if path in ("", "/api", "/api/health"):
            payload = {
                "status": "healthy",
                "service": "Junior Astronaut Mission Trainer - Python Science Layer",
                "schema_version": "1.1",
                "endpoints": [
                    "/api/mission-config",
                    "/api/scenarios/emergency",
                    "/api/fixtures/life-support",
                    "/api/fixtures/radiation"
                ]
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))
            return

        if path in ("/api/mission-config", "/api/config"):
            config_file = PROJECT_ROOT / "outputs" / "mission_config.json"
            if not config_file.exists():
                self._send_error(404, "mission_config.json not found. Run main.py first.")
                return
            with open(config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._set_headers(200)
            self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))
            return

        if path in ("/api/fixtures/life-support", "/api/fixtures/expected-life-support"):
            fixture_file = PROJECT_ROOT / "tests" / "fixtures" / "expected_life_support_calculations.json"
            if not fixture_file.exists():
                self._send_error(404, "Life support fixtures not found.")
                return
            with open(fixture_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._set_headers(200)
            self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))
            return

        if path in ("/api/fixtures/radiation", "/api/fixtures/expected-radiation"):
            fixture_file = PROJECT_ROOT / "tests" / "fixtures" / "expected_radiation_calculations.json"
            if not fixture_file.exists():
                self._send_error(404, "Radiation fixtures not found.")
                return
            with open(fixture_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._set_headers(200)
            self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))
            return

        if path in ("/api/scenarios/emergency", "/api/scenarios"):
            scenarios_file = PROJECT_ROOT / "outputs" / "emergency_scenarios.json"
            if not scenarios_file.exists():
                # On-the-fly generation from cached DONKI data
                try:
                    from src.ingestion.ingest_donki import fetch_donki_notifications
                    from src.processing.process_donki import parse_donki_notifications, clean_donki_events, filter_sep_scenarios
                    from src.mapping.map_donki_events import map_sep_events_to_scenarios
                    seps = filter_sep_scenarios(clean_donki_events(parse_donki_notifications(fetch_donki_notifications())))
                    scenarios = map_sep_events_to_scenarios(seps)
                except Exception as e:
                    self._send_error(500, f"Error generating scenarios: {e}")
                    return
            else:
                with open(scenarios_file, "r", encoding="utf-8") as f:
                    scenarios = json.load(f)
            self._set_headers(200)
            self.wfile.write(json.dumps({"scenarios": scenarios}, indent=2).encode("utf-8"))
            return

        self._send_error(404, f"Endpoint {path} not found.")

    def _send_error(self, code: int, message: str):
        self._set_headers(code)
        self.wfile.write(json.dumps({"error": message, "code": code}).encode("utf-8"))

    def log_message(self, format, *args):
        # Clean logging
        sys.stdout.write(f"[API Server] {self.address_string()} - {format % args}\n")
        sys.stdout.flush()


def run_server(port: int = 8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, MissionAPIHandler)
    print(f"======================================================================")
    print(f"  JUNIOR ASTRONAUT MISSION TRAINER — REST API SERVER")
    print(f"======================================================================")
    print(f"  Live Server listening at: http://localhost:{port}")
    print(f"  Endpoints available for TypeScript developer:")
    print(f"    • GET http://localhost:{port}/api/mission-config")
    print(f"    • GET http://localhost:{port}/api/scenarios/emergency")
    print(f"    • GET http://localhost:{port}/api/fixtures/life-support")
    print(f"    • GET http://localhost:{port}/api/fixtures/radiation")
    print(f"    • GET http://localhost:{port}/api/health")
    print(f"======================================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()


if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port)
