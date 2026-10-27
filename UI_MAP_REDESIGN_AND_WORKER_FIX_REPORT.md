# VARUNA 2047: India GIS Map Fix & Premium UI/UX Redesign Report

**Date:** October 27, 2026  
**Repository:** `D:\RACHIKA\HFS`  
**Platform:** VARUNA 2047 — National Earth Observation & Agricultural Climate Resilience  
**Scope:** Map Worker Bug Fix, Complete Visual India Map & Labels, Minimal Premium Navbar Redesign, Real GIS Dashboard Layout, and Platform-wide Consistency.

---

## 1. Exact Root Cause of the Worker Error

### The Error
`Console Error: Worker failed to load. Check that the worker URL is correct.`

### The Cause
MapLibre GL JS v6 (`maplibre-gl@6.16.0`) uses a dedicated Web Worker to parse GeoJSON datasets, generate vector tiles, triangulate polygon geometries, and layout text labels off the main thread.
Inside MapLibre (`src/util/web_worker.ts` lines 38–47):
```typescript
function defaultWorkerUrl(): string {
    const moduleUrl = import.meta.url;
    if (!/^https?:/.test(moduleUrl)) return '';
    const workerName = moduleUrl.endsWith('-dev.mjs')
        ? 'maplibre-gl-worker-dev.mjs'
        : 'maplibre-gl-worker.mjs';
    const url = new URL(`./${workerName}`, moduleUrl);
    url.searchParams.set('v', packageJSON.version);
    return url.href;
}
```
1. **Next.js Turbopack Bundler Behavior:** When Next.js bundles client components, `import.meta.url` evaluates to the client component chunk URL (e.g. `http://localhost:3000/_next/static/chunks/app/india/...`).
2. **404 Worker Request:** MapLibre attempted to instantiate `new Worker(url, {type: 'module'})` pointing to `http://localhost:3000/_next/static/chunks/app/india/maplibre-gl-worker.mjs`.
3. **MIME Type Mismatch:** Because Next.js does not serve raw node_modules files under `_next/static/chunks/`, the request returned a `404 Not Found` HTML document.
4. **Worker Failure Event:** When the browser worker engine failed to parse the 404 HTML response, MapLibre's `createActors` (`src/util/actor.ts:276`) intercepted the worker `error` event and dispatched:
   `errorTarget.fire(new ErrorEvent(new Error('Worker failed to load. Check that the worker URL is correct.')))`.
5. **Cascading Failure:** Because the worker aborted, MapLibre never tessellated or rendered the GeoJSON layers (`india_states.geojson` and `india_districts.geojson`), leaving the map looking like a plain dark background tile.

### The Fix
1. Copied the standalone MapLibre worker bundle `maplibre-gl-worker.mjs` (519 KB) directly into `frontend/public/maplibre/maplibre-gl-worker.mjs`.
2. Verified that Next.js serves it directly from the same origin at `http://localhost:3000/maplibre/maplibre-gl-worker.mjs` with `HTTP 200 OK` and `Content-Type: application/javascript; charset=UTF-8`.
3. Called `setWorkerUrl("/maplibre/maplibre-gl-worker.mjs")` in `frontend/components/IndiaMap.tsx` prior to map construction.
4. Ensured proper unmount cleanup (`map.remove()`, resetting refs) and guarded against SSR execution.

---

## 2. Files Modified

| File | Changes Made |
| :--- | :--- |
| [`frontend/components/IndiaMap.tsx`](file:///d:/RACHIKA/HFS/frontend/components/IndiaMap.tsx) | Configured `setWorkerUrl("/maplibre/maplibre-gl-worker.mjs")`; implemented 72/28 GIS dashboard layout; added visible state boundary fills (`#0f2b33`), hover (`#14b8a6`), and selection (`#0d9488`); added symbol text label layer for all 36 States/UTs; integrated 734 district outlines (`minzoom: 5.5`); added dynamic layer selector (Admin, ForestWatch loss, FSI canopy %, Monsoon rain); integrated real-time search filter and India reset control. |
| [`frontend/components/Navbar.tsx`](file:///d:/RACHIKA/HFS/frontend/components/Navbar.tsx) | Complete minimal premium redesign (64px single row); main navigation reduced to 4 primary items (`Overview`, `India Map`, `ForestWatch`, `Climate`) plus interactive `More` dropdown; removed bulky ISRO/NOAA boxes in favor of a sleek live data-status indicator; added responsive mobile navigation drawer. |
| [`frontend/app/india/page.tsx`](file:///d:/RACHIKA/HFS/frontend/app/india/page.tsx) | Updated Warangal ecological corridor card to reference verified Sentinel-2 MSI Tile `44QLE` and labeled the 236.21 ha disturbance strictly as *"Candidate vegetation disturbance detected from NDVI change"*. |
| [`frontend/app/india/[state]/[district]/page.tsx`](file:///d:/RACHIKA/HFS/frontend/app/india/[state]/[district]/page.tsx) | Updated satellite slider props to consume verified Sentinel-2 L2A BOA acquisition metadata and real before/after imagery paths. |
| [`frontend/app/layout.tsx`](file:///d:/RACHIKA/HFS/frontend/app/layout.tsx) | Set `html.dark` and body background to `bg-slate-950 text-slate-100` for consistent dark-theme visual quality across all routes. |
| [`frontend/app/globals.css`](file:///d:/RACHIKA/HFS/frontend/app/globals.css) | Standardized root variables to dark navy (`#020617`), modern system font stack, and custom sleek GIS scrollbars. |
| [`scripts/build_state_labels.py`](file:///d:/RACHIKA/HFS/scripts/build_state_labels.py) | Created automated pipeline to generate validated interior label points for all 36 Indian States and Union Territories with cartographic rank tiers. |
| [`frontend/public/data/india_state_labels.geojson`](file:///d:/RACHIKA/HFS/frontend/public/data/india_state_labels.geojson) | Exported 36 validated point features for MapLibre WebGL text rendering. |
| [`frontend/public/maplibre/maplibre-gl-worker.mjs`](file:///d:/RACHIKA/HFS/frontend/public/maplibre/maplibre-gl-worker.mjs) | Deployed local same-origin Web Worker script. |
| [`frontend/public/fonts/`](file:///d:/RACHIKA/HFS/frontend/public/fonts/) | Hosted local font PBF glyphs (`0-255.pbf`) for offline WebGL label rendering. |

---

## 3. Visual & Aesthetic Enhancements

### 3.1 State Boundaries & State Names
- **State Boundaries:** Every one of the 28 States and 8 Union Territories is rendered using validated polygons from Survey of India (SOI) / Registrar General of India (RGI) 2019 dataset.
- **Palette:**
  - Default fill: Tasteful dark teal-navy (`#0f2b33`, 40% opacity).
  - Outlines: Crisp cyan-teal (`#14b8a6`, 1.2px width).
  - Hover highlight: Vivid teal (`#14b8a6`, 55% opacity, 2.0px border).
  - Selected state: Rich turquoise (`#0d9488`, 75% opacity, `#5eead4` 2.5px border).
- **State Names:** Visible labels rendered via MapLibre symbol layer using validated interior representative points. Labels feature high-contrast `#f8fafc` text with dark `#091522` halo, collision avoidance, and progressive zoom scaling.
- **District Outlines:** Automatically become visible at zoom $\ge 5.5$ or when a state is selected, styled with thin contrasting sky blue lines (`#38bdf8`, 0.8px, dasharray `[2, 1]`).

### 3.2 Real GIS Dashboard Layout (72% Map / 28% Panel)
- **Left Map Viewport (~72% width):** Large interactive MapLibre map with full India framing (`fitBounds`), Esri World Dark Gray basemap, floating search bar, layer tabs, and dynamic legend.
- **Right Regional Intelligence Panel (~28% width):**
  - **National Mode (Default):** Displays national ISFR baseline forest cover (21.71%, 7,13,789 sq km), sensor cadence (Sentinel-2 10m & Landsat 30m), and interactive drilldown guidance.
  - **State Mode:** Displays state administrative details, FSI forest baseline, annual loss, district count, and scrollable district directory with instant click-to-zoom.
  - **District Mode:** Displays district profile, area, forest baseline, candidate vegetation disturbance (properly qualified), monsoon normal rainfall, direct link to Regional Workspace (`/india/[state]/[district]`), and Research Dossier generation.

### 3.3 Minimal Premium Navbar
- **Height:** 64px (`h-16`) single-row desktop layout.
- **Branding:** `VARUNA 2047` in crisp bold white with teal-400 accent, earth satellite glyph, and subtitle `National Earth Intelligence`.
- **Primary Routes:** Direct access to `Overview` (`/`), `India Map` (`/india`), `ForestWatch` (`/forestwatch`), and `Climate` (`/enso`).
- **More Dropdown:** Clean popup containing `EO Explorer`, `AI Risk Lab`, `Resilience Planner`, `Evidence Reports`, and `Research & Provenance`.
- **Status Indicator:** Replaced bulky boxes with a compact live service status badge (`Data Hub: Verified Active` with pulsing green dot).
- **Mobile Menu:** Accessible drawer with organized primary and secondary navigation sections.

---

## 4. API Keys & Configuration Requirements

> [!NOTE]
> **Zero external API keys are required to run VARUNA 2047!**
> 
> - **Basemap:** Powered by **Esri World Dark Gray Canvas** (`https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}`), which is completely **free and requires no API key**.
> - **Sentinel-2 L2A STAC Satellite Imagery:** Hosted on the public AWS Open Data Sponsorship Program (`https://sentinel-cogs.s3.us-west-2.amazonaws.com`), requiring **no API key**.
> - **India Administrative Boundaries (36 States, 734 Districts):** Bundled locally as GeoJSON assets, requiring **no API key**.
> - **Font Glyphs:** Bundled locally under `/public/fonts/`, requiring **no API key**.
> - **Optional Future Keys:** If you ever decide to switch to proprietary commercial basemaps (e.g. Mapbox Vector Streets or Carto Custom Styles), you can set `NEXT_PUBLIC_MAPBOX_TOKEN=pk.xxx` in `frontend/.env.local`. For all currently implemented features, no API key is necessary.

---

## 5. Verification & Audit Results

### 5.1 Automated Backend & Geospatial Test Suite
```powershell
pytest -v tests/
====================== 35 passed, 17 warnings in 10.71s ======================
```
- `tests/backend/test_api.py`: 12 passed
- `tests/backend/test_india_forest_api.py`: 14 passed
- `tests/geospatial/test_engine.py`: 4 passed
- `tests/geospatial/test_forest_engine.py`: 5 passed

### 5.2 Next.js Production Build
```
npm run build
▲ Next.js 16.4.3 (Turbopack)
✓ Running next.config.ts took 99ms
✓ Compiled successfully in 6.6s
✓ Finished TypeScript in 8.9s
✓ Generating static pages (14/14) in 4.1s
```
Zero linting, TypeScript, or bundling errors across all 14 application routes.

### 5.3 Live Service Endpoints Audit
Execution of [`scripts/audit_live_endpoints.py`](file:///d:/RACHIKA/HFS/scripts/audit_live_endpoints.py) confirmed:
- **All 32 Backend Endpoints:** Returning `HTTP 200 OK`.
- **All 11 Frontend Pages:** Returning `HTTP 200 OK`.
- **Map Worker & Assets:**
  - `GET /maplibre/maplibre-gl-worker.mjs` $\to$ `HTTP 200 OK` (519 KB)
  - `GET /data/india_states.geojson` $\to$ `HTTP 200 OK` (58 KB)
  - `GET /data/india_state_labels.geojson` $\to$ `HTTP 200 OK` (14 KB)
  - `GET /data/india_districts.geojson` $\to$ `HTTP 200 OK` (6.26 MB)

---

## 6. Summary of Resolutions

1. **Worker Error:** Fixed at root by deploying `maplibre-gl-worker.mjs` to same-origin `/maplibre/` and configuring `setWorkerUrl`.
2. **State Boundaries & Names:** Fully visible and selectable for all 28 states and 8 UTs with interior representative label points.
3. **National Framing:** India centered with `fitBounds`, accommodating the right-side dashboard panel.
4. **Navigation:** Minimal 64px navbar with 4 primary links and a curated `More` dropdown.
5. **GIS Dashboard Layout:** 72/28 split with complete administrative, forest, and climate inspection.
6. **Scientific Rigor:** Candidate vegetation disturbance strictly designated as detected from NDVI change (236.21 ha in Warangal), with zero invented tree counts or cross-state model leakage.
