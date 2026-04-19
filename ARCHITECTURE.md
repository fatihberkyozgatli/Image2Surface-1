# Image2Surface Architecture Documentation

## Overview

Image2Surface implements two distinct architectural patterns to demonstrate different design approaches for the same problem domain. This document outlines both architectures, their component structure, class organization, and implementation details.

## Architecture 1: Layered Architecture (SELECTED)

### Architectural Pattern Description

The Selected implementation uses a **Layered Architecture**, organizing the system into distinct horizontal layers where each layer provides services only to the layer directly above it. This pattern emphasizes separation of concerns through vertical organization.

### Layer Structure

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 5: Presentation Layer                                 │
│ (Next.js React Components, UI)                              │
├─────────────────────────────────────────────────────────────┤
│ Layer 4: Communication Layer                                │
│ (Axios HTTP Client, API Type Definitions)                   │
├─────────────────────────────────────────────────────────────┤
│ Layer 3: API Layer                                          │
│ (FastAPI Routes, Request/Response Models)                   │
├─────────────────────────────────────────────────────────────┤
│ Layer 2: Business Logic Layer                               │
│ (Processing Modules, Application Logic)                     │
├─────────────────────────────────────────────────────────────┤
│ Layer 1: Data/Infrastructure Layer                          │
│ (File System, Model Checkpoints, Storage)                   │
└─────────────────────────────────────────────────────────────┘
```

### Component Diagram (Layered)

```
┌───────────────────────┐
│   Image Upload UI     │
│   + Preview Display   │
│   + Edit Controls     │
│   + 3D Viewer         │
└───────────────────────┘
          ↕ (HTTP)
┌───────────────────────┐
│  REST API Endpoints   │
│  · /upload            │
│  · /generate          │
│  · /edit              │
│  · /reset             │
└───────────────────────┘
          ↕
┌───────────────────────┐
│  Processing Engines   │
│  · image processing   │
│  · depth estimation   │
│  · mesh generation    │
│  · mesh editing       │
└───────────────────────┘
          ↕
┌───────────────────────┐
│  Deep Learning Model  │
│  (Depth Anything V2)  │
└───────────────────────┘
          ↕
┌───────────────────────┐
│  File System Storage  │
│  · Images             │
│  · Checkpoints        │
└───────────────────────┘
```

### Class Structure (Layered)

```
PRESENTATION LAYER
├── App Component (page.tsx)
│   ├── State Management
│   └── Screen Navigation
└── UI Components
    ├── ImageUpload
    ├── SurfaceViewer
    ├── EditControls
    └── Shadcn/UI Components

COMMUNICATION LAYER
└── API Client (api.ts)
    ├── uploadImage()
    ├── generateSurface()
    ├── editSurface()
    ├── resetSurface()
    └── healthCheck()

API LAYER
└── FastAPI Application (server.py)
    ├── @app.post("/api/image/upload")
    ├── @app.post("/api/surface/generate")
    ├── @app.post("/api/surface/edit")
    ├── @app.post("/api/surface/reset")
    └── Pydantic Models
        ├── ImageUploadResponse
        ├── SurfaceGenerateResponse
        ├── EditResponse
        └── ResetResponse

BUSINESS LOGIC LAYER
├── application.py
│   ├── save_obj()
│   ├── generate_surface()
│   └── export_mesh()
└── processing.py
    ├── load_model()
    ├── estimate_depth()
    ├── downsample_depth()
    ├── smooth_depth()
    ├── compute_vertices()
    ├── normalize_coordinate_space()
    └── [Mesh editing functions]

DATA LAYER
├── File System
│   ├── UPLOAD_DIR
│   ├── CHECKPOINT_DIR
│   └── OUTPUT_DIR
└── PyTorch Model
    └── Depth Anything V2
```

### Component-to-Class Mapping (Layered)

| Component | Implementing Classes | Location |
|-----------|---------------------|----------|
| Image Upload UI | ImageUpload component | frontend/components/image-upload.tsx |
| Surface Viewer | SurfaceViewer component | frontend/components/surface-viewer.tsx |
| Edit Controls | EditControls component | frontend/components/edit-controls.tsx |
| HTTP Client | api.ts functions | frontend/lib/api.ts |
| Type Definitions | Typescript interfaces | frontend/lib/types.ts |
| API Routes | FastAPI decorators | backend/server.py |
| Response Models | Pydantic BaseModel classes | backend/server.py |
| Image Processing | Functions in processing.py | backend/processing.py |
| Mesh Generation | Functions in application.py | backend/application.py |
| Storage Management | Directory operations | backend/server.py, application.py |

---

## Architecture 2: Model-View-Controller Architecture (UNSELECTED)

### Architectural Pattern Description

The Unselected implementation uses a **Model-View-Controller (MVC) Architecture**, separating the system into three interconnected components: Models (data/business logic), Views (UI), and Controllers (request handlers). This pattern emphasizes the interaction between data, presentation, and control logic.

### MVC Structure

```
┌──────────────┐
│   Views      │
│  (Frontend)  │
└──────┬───────┘
       │ HTTP Request
       ↓
┌──────────────────────────┐
│   Controllers            │
│ (Route Handlers)         │
│ · HealthController       │
│ · ImageController        │
│ · SurfaceController      │
└──────┬───────────────────┘
       │ Calls
       ↓
┌──────────────────────────┐
│   Services               │
│ (Business Logic)         │
│ · ImageService           │
│ · DepthService           │
│ · MeshService            │
└──────┬───────────────────┘
       │ Operates on
       ↓
┌──────────────────────────┐
│   Models                 │
│ (Domain Objects)         │
│ · ImageModel             │
│ · MeshModel              │
│ · DepthEstimationModel   │
└──────┬───────────────────┘
       │ Persists to
       ↓
┌──────────────────────────┐
│ Data Store               │
│ (File System)            │
└──────────────────────────┘
```

### Component Diagram (MVC)

```
┌─────────────────────────┐
│      VIEWS              │
│   React Components      │
│   (Same as Selected)    │
└────────────┬────────────┘
             │ HTTP
             ↓
┌─────────────────────────────────────┐
│         CONTROLLERS                 │
│  HealthController                   │
│  ├── /api/health                    │
│  ImageController                    │
│  ├── /api/image/upload              │
│  SurfaceController                  │
│  ├── /api/surface/generate          │
│  ├── /api/surface/edit              │
│  └── /api/surface/reset             │
└────────────┬────────────────────────┘
             │ Delegates to
             ↓
┌─────────────────────────────────────┐
│         SERVICES                    │
│  ImageService                       │
│  ├── save_uploaded_image()          │
│  ├── load_image()                   │
│  └── validate_image_format()        │
│  DepthService                       │
│  ├── estimate_depth()               │
│  ├── process_depth_map()            │
│  └── estimate_and_process()         │
│  MeshService                        │
│  ├── generate_mesh_from_depth()     │
│  ├── smooth_mesh()                  │
│  ├── sharpen_mesh()                 │
│  └── scale_mesh()                   │
└────────────┬────────────────────────┘
             │ Operates on
             ↓
┌─────────────────────────────────────┐
│         MODELS                      │
│  ImageModel                         │
│  ├── image_id, filename, file_path  │
│  ├── width, height, format          │
│  └── Methods: exists(), delete()    │
│  MeshModel                          │
│  ├── vertices[], faces[]            │
│  ├── vertex_colors, original_state  │
│  └── Methods: reset(), save_orig()  │
│  DepthEstimationModel               │
│  ├── z_scale, smooth_strength       │
│  ├── downsample_scale, encoder      │
│  └── Methods: validate(), config()  │
└────────────┬────────────────────────┘
             │ Stored in
             ↓
┌─────────────────────────────────────┐
│  DATA STORE                         │
│  File System Storage                │
└─────────────────────────────────────┘
```

### Class Structure (MVC)

```
VIEWS
├── Next.js React Components
│   └── (Same as Selected architecture)

CONTROLLERS
├── controllers/__init__.py
├── controllers/health_controller.py
│   └── HealthController
│       └── GET /api/health
├── controllers/image_controller.py
│   └── ImageController
│       └── POST /api/image/upload
└── controllers/surface_controller.py
    └── SurfaceController
        ├── POST /api/surface/generate
        ├── POST /api/surface/edit
        └── POST /api/surface/reset

SERVICES
├── services/__init__.py
├── services/image_service.py
│   └── ImageService (static methods)
│       ├── save_uploaded_image()
│       ├── load_image()
│       ├── delete_image()
│       └── validate_image_format()
├── services/depth_service.py
│   └── DepthService (static methods)
│       ├── load_model()
│       ├── estimate_depth()
│       ├── process_depth_map()
│       └── estimate_and_process()
└── services/mesh_service.py
    └── MeshService (static methods)
        ├── generate_mesh_from_depth()
        ├── smooth_mesh()
        ├── sharpen_mesh()
        ├── scale_mesh()
        └── _build_adjacency()

MODELS
├── models/__init__.py
├── models/image_model.py
│   └── ImageModel
│       ├── Properties: image_id, filename, file_path, width, height, format
│       ├── get_file_content()
│       ├── exists()
│       └── delete()
├── models/mesh_model.py
│   ├── Vertex
│   │   ├── x, y, z
│   │   ├── to_tuple()
│   │   └── to_list()
│   ├── Face
│   │   ├── v0, v1, v2
│   │   ├── to_tuple()
│   │   └── to_list()
│   └── MeshModel
│       ├── vertices[], faces[], vertex_colors
│       ├── original_vertices[]
│       ├── get_vertex_count()
│       ├── get_face_count()
│       ├── get_bounds()
│       ├── to_dict()
│       ├── reset_to_original()
│       └── save_original()
└── models/depth_model.py
    └── DepthEstimationModel
        ├── z_scale, smooth_strength, downsample_scale, encoder
        ├── depth_map
        ├── validate()
        └── get_config()
```

### Component-to-Class Mapping (MVC)

| Component | Implementing Classes | Location |
|-----------|---------------------|----------|
| Views (UI) | React components | frontend/components/ |
| Health Controller | HealthController | backend_mvc/controllers/health_controller.py |
| Image Controller | ImageController | backend_mvc/controllers/image_controller.py |
| Surface Controller | SurfaceController | backend_mvc/controllers/surface_controller.py |
| Image Service | ImageService | backend_mvc/services/image_service.py |
| Depth Service | DepthService | backend_mvc/services/depth_service.py |
| Mesh Service | MeshService | backend_mvc/services/mesh_service.py |
| Image Model | ImageModel | backend_mvc/models/image_model.py |
| Mesh Model | MeshModel, Vertex, Face | backend_mvc/models/mesh_model.py |
| Depth Model | DepthEstimationModel | backend_mvc/models/depth_model.py |
| Main App | FastAPI app | backend_mvc/app.py |

---

## Data Flow Comparison

### Selected Architecture (Layered)

```
User Action
    ↓
Front-end Component
    ↓
API Client (Axios)
    ↓
HTTP Request → /api/surface/generate
    ↓
FastAPI Route Handler
    ↓
Call processing.process_image()
    ↓
Depth Estimation
    ↓
Call application.generate_surface()
    ↓
Mesh Computation
    ↓
Return vertices & indices
    ↓
Pydantic Response Model
    ↓
JSON Response
    ↓
Front-end State Update
    ↓
Three.js Renderer
    ↓
Display 3D Mesh
```

### Unselected Architecture (MVC)

```
User Action
    ↓
View Component
    ↓
HTTP Request
    ↓
Controller (SurfaceController.generate_surface)
    ↓
Calls DepthService.estimate_and_process()
    ↓
DepthService uses DepthEstimationModel config
    ↓
Depth Estimation + Processing
    ↓
Calls MeshService.generate_mesh_from_depth()
    ↓
MeshService operates on MeshModel
    ↓
Creates Vertex[] and Face[] in MeshModel
    ↓
MeshModel.to_dict()
    ↓
Response Model (MeshData)
    ↓
JSON Response
    ↓
View State Update
    ↓
Three.js Renderer
    ↓
Display 3D Mesh
```

---

## Technology Stack Consistency

Both architectures use identical technology stacks:

### Frontend
- Next.js 14
- React 18
- TypeScript
- Three.js & React Three Fiber
- Tailwind CSS
- Axios

### Backend Infrastructure
- Python 3.8+
- FastAPI 0.104+
- Uvicorn 0.24+
- PyTorch 2.0+
- OpenCV 4.8+
- NumPy 1.24+

### Shared Model
- Depth Anything V2 (same weights file)
- Same import/export functionality

---

## Key Architectural Differences Summary

| Aspect | Layered | MVC |
|--------|----------------|-----|
| Organization | Horizontal layers | M-V-C separation |
| Emphasis | Layer separation | Component roles |
| Request Flow | Cascades through layers | Controller coordinates |
| Business Logic | In processing modules | In services |
| Data Objects | Implicit dictionaries | Explicit model classes |
| Abstraction | Multiple layers | Direct model access |
| Code Structure | Flatter organization | More structured folders |
| Extensibility | Add new layers | Add new M/V/C |
| Testability | Layer-level tests | Component-level tests |

