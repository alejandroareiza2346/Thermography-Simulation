# Thermography-Simulation
**Engineering Lead: Alejandro Areiza Alzate**
**Technical Domain: Computer Vision / Scientific Image Processing / Industrial Sensing Simulation**

---

## 1. Executive Summary and Architectural Vision

This project implements a **thermal image simulation engine** that transforms standard grayscale images into false-color thermographic representations using OpenCV's colormap pipeline. The system applies a user-selectable false-color map (JET, HOT, COOL, RAINBOW, OCEAN) to grayscale pixel intensity values, treating luminance as a proxy for thermal emission intensity — the same encoding principle used in real infrared camera output formats (FLIR Radiometric JPEG, IRI). A configurable hot-zone detection layer segments and annotates regions exceeding a threshold intensity value, replicating the anomaly highlighting behavior of commercial thermographic analysis software. The architecture centers on the `TermografiaSimulator` class, which encapsulates the full processing pipeline as a reusable programmatic API, while `termografia_simulation.py` exposes it through a full-featured argparse CLI. The `ejemplos_demo.py` module provides six end-to-end demonstration scenarios covering different colormap and threshold configurations.

---

## 2. Requirement Analysis and Strategic Alignment

- **Functional:** Colormap application to grayscale images via `cv2.applyColorMap()` with support for five thermal false-color maps (JET, HOT, COOL, RAINBOW, OCEAN); configurable intensity threshold for hot-zone segmentation (0–255, default 200); contour detection and white-border annotation of high-intensity regions; side-by-side display of original, grayscale, and thermographic output; CLI flags for threshold adjustment, colormap selection, output filename, headless batch mode (`--no-mostrar`), save suppression (`--no-guardar`), and hot-zone highlighting suppression (`--no-resaltar`); programmatic API via `TermografiaSimulator` class for embedding in larger computer vision pipelines; installation verification script (`verificar_instalacion.py`).
- **Non-Functional:** Zero-latency colormap rendering — `cv2.applyColorMap` operates in O(W×H) time on the pixel array with no iterative Python loops; compatible with JPG and PNG input formats; headless execution support for server and CI/CD environments via `--no-mostrar`; no GPU or CUDA dependency — runs on any Python 3.7+ environment.
- **Strategic Goal:** A functional simulation layer for validating thermographic analysis logic, developing industrial inspection UI prototypes, and generating synthetic thermal datasets for computer vision model training — without requiring access to physical infrared hardware.

---

## 3. Technical Stack and Infrastructure

- **Core Language:** Python 3.7+
- **Computer Vision:** OpenCV (`cv2`) — `applyColorMap`, `findContours`, `drawContours`, `cvtColor`, `threshold`, `imread`, `imshow`, `imwrite`
- **Numerical Computing:** NumPy — pixel array manipulation, mask generation for threshold segmentation
- **CLI Interface:** `argparse` — full-featured command-line interface with positional and optional arguments
- **Execution Environment:** Windows, Linux, macOS; headless server environments supported via `--no-mostrar` flag
- **Design Pattern:** Object-Oriented encapsulation — `TermografiaSimulator` class manages image state and exposes the processing pipeline as discrete, chainable methods (`cargar_imagen`, `aplicar_mapa_termico`, `resaltar_zonas_calientes`, `mostrar_imagenes`, `guardar_resultado`), enabling programmatic integration without instantiating the CLI

---

## 4. Engineering Logic and Implementation

The simulation pipeline operates in six sequential steps:

**Step 1 — Image Load and Grayscale Conversion:** The input image is loaded with `cv2.imread()` and converted to grayscale via `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`. Grayscale pixel values (0–255) serve as the thermal intensity proxy — darker pixels map to lower temperatures, brighter pixels to higher temperatures — consistent with the luminance-temperature mapping convention used in thermal camera output.

**Step 2 — Colormap Application:** `cv2.applyColorMap(gray_image, colormap_constant)` maps each 8-bit grayscale value to a 3-channel BGR color according to the selected false-color palette:

| Colormap | OpenCV Constant | Thermal Convention |
|---|---|---|
| JET | `cv2.COLORMAP_JET` | Blue (cold) → green → yellow → red (hot) |
| HOT | `cv2.COLORMAP_HOT` | Black → red → yellow → white |
| COOL | `cv2.COLORMAP_COOL` | Cyan → magenta |
| RAINBOW | `cv2.COLORMAP_RAINBOW` | Full visible spectrum |
| OCEAN | `cv2.COLORMAP_OCEAN` | Blue-green tonal range |

This is a per-pixel lookup table operation with O(W×H) complexity and no iterative Python processing — the entire colormap is applied in a single vectorized C++ call within OpenCV.

**Step 3 — Hot-Zone Threshold Segmentation:** `cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)` produces a binary mask where pixels above the threshold value are set to 255 (white) and all others to 0. This mask isolates the high-intensity regions that correspond to thermally anomalous zones in a real infrared image.

**Step 4 — Contour Detection:** `cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)` extracts the external boundaries of all connected white regions in the binary mask. Only external contours are retrieved (`RETR_EXTERNAL`), preventing nested contour artifacts on complex hot-zone shapes.

**Step 5 — Annotation:** `cv2.drawContours(thermal_image, contours, -1, (255, 255, 255), 2)` draws 2-pixel white borders around all detected hot-zone contours on the colormap-applied output image, replicating the anomaly annotation behavior of commercial thermographic software.

**Step 6 — Output:** The result is displayed via `cv2.imshow()` in a three-panel layout (original, grayscale, thermographic) and written to disk with `cv2.imwrite()`.

- **Complexity:** O(W×H) for colormap application and thresholding; O(k) for contour retrieval where k is the number of detected contour points; all pixel-level operations execute in native C++ within OpenCV with no Python-level iteration.
- **Data Structures:** NumPy `ndarray` for all image representations; list of contour coordinate arrays (`np.ndarray`) returned by `findContours`.

---

## 5. Quality Assurance and Systematic Testing

- **Analytical Testing:** Colormap constant mapping table verified against OpenCV documentation — each string key (`"jet"`, `"hot"`, `"cool"`, `"rainbow"`, `"ocean"`) resolves to its correct `cv2.COLORMAP_*` integer constant in the dispatcher dictionary; threshold range validated to accept only values in [0, 255] via `argparse` type constraints.
- **Constructive Testing:** Six demonstration scenarios in `ejemplos_demo.py` validate end-to-end behavior across different colormap and threshold combinations: `demo_basico` (default JET, threshold 200), `demo_diferentes_mapas` (all five colormaps on the same input), `demo_umbral_personalizado` (threshold sweep at 150, 180, 220), `demo_sin_resaltado` (colormap only, no contour annotation), `demo_modo_batch` (headless execution without display windows), and `demo_api_programatica` (direct `TermografiaSimulator` class usage).
- **Edge Case Handlers:** Image not found at specified path — `cv2.imread()` returns `None`; the simulator raises a structured `ValueError` with the provided path before any processing occurs; input image already in grayscale — `cvtColor` handles single-channel inputs without raising an exception; threshold value of 0 — entire image flagged as hot zone; threshold value of 255 — no hot zones detected; headless environment — `--no-mostrar` suppresses all `cv2.imshow()` calls, preventing `DISPLAY` environment errors on Linux servers.
- **Verification Script:** `verificar_instalacion.py` confirms that `cv2`, `numpy`, and the expected OpenCV version are importable and functional before the main simulator is run.

---

## 6. Security Governance and Compliance

- **Input Handling:** All user-supplied arguments are typed and validated by `argparse` — the image path is treated as a filesystem read target only; the threshold value is cast to `int` with range enforcement; the colormap name is resolved through a fixed dictionary of five valid keys, rejecting any unrecognized string before it reaches OpenCV.
- **No Dynamic Execution:** No `eval()`, `exec()`, or shell command construction from user input. Image processing is performed entirely through OpenCV's native C++ layer via the Python bindings.
- **Local Execution:** No network connections, external API calls, or telemetry. All image data remains local to the execution environment. The system is suitable for processing sensitive industrial or medical imagery without data exfiltration risk.
- **Headless Deployment:** `--no-mostrar` and `--no-guardar` flags enable fully non-interactive execution in CI/CD pipelines, server-side batch jobs, or containerized environments without X11 or display server requirements.

---

## 7. Deployment and Initialization

**Prerequisites:** Python 3.7+

```bash
# Clone the repository
git clone https://github.com/alejandroareiza2346/Thermography-Simulation.git

cd Thermography-Simulation

# Install dependencies
pip install -r requirements.txt

# Verify installation
python verificar_instalacion.py
```

**Basic usage:**

```bash
# Apply default JET colormap with threshold 200
python termografia_simulation.py ejemplos/imagen_ejemplo.jpg

# Adjust hot-zone threshold
python termografia_simulation.py imagen.jpg --umbral 180

# Select colormap
python termografia_simulation.py imagen.jpg --mapa hot

# Custom output filename
python termografia_simulation.py imagen.jpg --salida resultado_termico.jpg

# Headless batch mode (no display windows)
python termografia_simulation.py imagen.jpg --no-mostrar

# Colormap only — suppress hot-zone annotation
python termografia_simulation.py imagen.jpg --no-resaltar
```

**Programmatic API:**

```python
import cv2
from termografia_simulation import TermografiaSimulator

sim = TermografiaSimulator()
sim.cargar_imagen("input.jpg")
sim.aplicar_mapa_termico(cv2.COLORMAP_HOT)
sim.resaltar_zonas_calientes(umbral=180)
sim.mostrar_imagenes()
sim.guardar_resultado("thermal_output.jpg")
```

**Run all demonstration scenarios:**

```bash
python ejemplos_demo.py
```

---

## 8. CLI Reference

| Argument | Type | Default | Description |
|---|---|---|---|
| `imagen` | `str` | Required | Path to input image (JPG or PNG) |
| `--umbral` | `int` | `200` | Intensity threshold for hot-zone segmentation (0–255) |
| `--mapa` | `str` | `jet` | False-color map: `jet`, `hot`, `cool`, `rainbow`, `ocean` |
| `--salida` | `str` | `termografia_resultado.jpg` | Output file path |
| `--no-resaltar` | flag | `False` | Suppress hot-zone contour annotation |
| `--no-mostrar` | flag | `False` | Suppress `cv2.imshow()` display windows |
| `--no-guardar` | flag | `False` | Suppress output file write |

---

## 9. Repository Structure

```
Thermography-Simulation/
├── .vscode/                        # VS Code workspace settings
├── ejemplos/
│   ├── imagen_ejemplo.jpg          # Sample input image
│   └── resultado_ejemplo.jpg       # Sample thermographic output
├── termografia_simulation.py       # TermografiaSimulator class + argparse CLI
├── ejemplos_demo.py                # Six end-to-end demonstration scenarios
├── verificar_instalacion.py        # Dependency verification script
├── requirements.txt                # opencv-python, numpy
└── README.md                       # Project documentation
```

---

## 10. Professional Background

Project designed and developed by **Alejandro Areiza Alzate**, Computer Engineering student at Universidad Autónoma Latinoamericana (UNAULA), Medellín, and GitHub Developer Program member.

- **LinkedIn:** [linkedin.com/in/alejandro-areiza-alzate-8a73a53b4](https://www.linkedin.com/in/alejandro-areiza-alzate-8a73a53b4)
- **Research (ORCID):** [0009-0002-2116-6918](https://orcid.org/0009-0002-2116-6918)
- **Certifications:** Microsoft Learn Level 6 — 26,950 XP (Azure Identity, Network Security & SQL Security); Cisco; Google; IBM; OWASP Top 10

---

## 11. License

Distributed under the **MIT License**. See `LICENSE` for full terms.
