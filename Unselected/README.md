# Image2Surface - Unselected Architecture (Model-View-Controller)

Convert 2D images to interactive 3D surface meshes using AI-powered depth estimation (Depth Anything V2).

## Overview

Image2Surface is a full-stack application that estimates depth information from 2D images and converts them into interactive 3D surface meshes. **This is the UNSELECTED implementation using a Model-View-Controller (MVC) Architecture**, emphasizing explicit domain modeling with coordinated request handling through controllers and services.

The system consists of a modern web-based frontend built with Next.js and a Python-based backend API powered by FastAPI, utilizing deep learning models for pixel-level depth prediction.

## System Capabilities

The application provides the following core capabilities:

1. **Image Upload**: Users can upload 2D images in standard image formats
2. **Depth Estimation**: Automated depth prediction using the Depth Anything V2 model
3. **Mesh Generation**: Conversion of estimated depth maps to 3D triangulated surface meshes
4. **Mesh Interaction**: Real-time 3D visualization with rotation, zoom, and pan controls
5. **Mesh Editing**: Apply smoothing, sharpening, and scaling operations to generated meshes
6. **Mesh Reset**: Restore original mesh before any edits

## Project Structure

```
Unselected/
├── backend/
│   ├── app.py                 # FastAPI application setup (MVC Coordinator)
│   ├── controllers/           # Request handlers and orchestration
│   │   ├── health_controller.py
│   │   ├── image_controller.py
│   │   └── surface_controller.py
│   ├── models/                # Domain models and data structures
│   │   ├── image_model.py
│   │   ├── mesh_model.py
│   │   └── depth_model.py
│   ├── services/              # Business logic and operations
│   │   ├── image_service.py
│   │   ├── depth_service.py
│   │   └── mesh_service.py
│   ├── depth_anything_v2/     # Depth estimation model implementation
│   │   ├── dpt.py
│   │   ├── dinov2.py
│   │   └── dinov2_layers/
│   ├── checkpoints/           # Model weights directory
│   ├── uploads/               # Temporary image storage
│   ├── venv/                  # Python virtual environment
│   └── requirements.txt       # Python dependencies
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx           # Main application page (View Layer)
│   │   ├── layout.tsx         # Root layout
│   │   └── globals.css        # Global styles
│   ├── components/
│   │   ├── image-upload.tsx   # Image upload component
│   │   ├── surface-viewer.tsx # 3D viewer component
│   │   ├── edit-controls.tsx  # Mesh editing controls
│   │   └── ui/                # Reusable UI components
│   ├── lib/
│   │   ├── api.ts             # API client abstraction (Communication Layer)
│   │   ├── types.ts           # TypeScript type definitions
│   │   └── utils.ts           # Utility functions
│   ├── package.json           # Node.js dependencies
│   └── node_modules/          # Installed npm packages
│
└── README.md                  # This file
```

## Architecture: Model-View-Controller Pattern (UNSELECTED)

### Architectural Rationale

The **Model-View-Controller (MVC) Architecture** was evaluated because:

- **Explicit domain modeling**: Models are first-class domain objects
- **Coordinated request handling**: Controllers orchestrate business logic
- **Reusable services**: Business logic is centralized and sharable
- **Clear folder structure**: Instant understanding of codebase organization
- **Type-safe operations**: Models carry both data and behavior

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│ View Layer (Frontend)                                        │
│ Next.js 14 React Application with TypeScript & Tailwind    │
├─────────────────────────────────────────────────────────────┤
│ - ImageUpload: File selection and preview                  │
│ - SurfaceViewer: 3D visualization with Three.js            │
│ - EditControls: Mesh editing operations                    │
│ - UI Components: Buttons, sliders, controls                │
├─────────────────────────────────────────────────────────────┤
│ Communication Layer                                         │
│ Axios HTTP Client with REST API Abstraction                │
├─────────────────────────────────────────────────────────────┤
│ Controller Layer (Backend)                                  │
│ Route Handlers Orchestrating Request Processing            │
│ - ImageController: Handles image operations               │
│ - SurfaceController: Orchestrates mesh workflows           │
│ - HealthController: System health checks                   │
├─────────────────────────────────────────────────────────────┤
│ Service Layer (Business Logic)                              │
│ - ImageService: Image operations and validation            │
│ - DepthService: Depth estimation pipeline                  │
│ - MeshService: Mesh generation and editing                 │
├─────────────────────────────────────────────────────────────┤
│ Model Layer (Domain Objects)                                │
│ - ImageModel: Image representation and metadata            │
│ - MeshModel: Mesh structure with vertices/faces            │
│ - DepthModel: Depth map and processing state               │
├─────────────────────────────────────────────────────────────┤
│ Infrastructure Layer                                        │
│ PyTorch models, OpenCV, file system, storage               │
└─────────────────────────────────────────────────────────────┘
```

### Component Interactions (MVC)

1. **View → Controller**: User action triggers HTTP request
2. **Controller**: Routes request to appropriate service
3. **Service → Model**: Business logic creates/manipulates domain objects
4. **Model**: Domain objects encapsulate data and operations
5. **Service**: Business logic orchestrates object interactions
6. **Controller**: Formats response from models
7. **Communication → View**: Response flows back to user

### Data Flow

1. User uploads image through web interface (View)
2. Frontend sends image to backend via HTTP (Communication)
3. ImageController receives POST request and delegates
4. ImageService validates and processes image
5. ImageModel created with metadata
6. Controller returns response (Model serialized to JSON)
7. User triggers mesh generation
8. SurfaceController receives POST with image_id
9. SurfaceController delegates to MeshService
10. MeshService uses DepthService for estimation
11. MeshModel created with vertices and indices
12. Models are serialized and returned to View
13. Three.js renders mesh (View)
14. Editing requests follow controller → service → model chain

## Technology Stack

### Backend Technologies

- **Python 3.13** (Programming language)
- **FastAPI 0.104+** (Web framework for RESTful API)
- **Uvicorn 0.24+** (ASGI server)
- **PyTorch 2.0+** (Deep learning framework)
- **OpenCV 4.8+** (Computer vision library)
- **NumPy 1.24+** (Numerical computing)

### Frontend Technologies

- **Next.js 16** (React framework with TypeScript)
- **React 18** (UI library)
- **TypeScript 5** (Type-safe JavaScript)
- **Three.js** (3D graphics library)
- **React Three Fiber** (React renderer for Three.js)
- **Tailwind CSS 3** (Utility-first CSS framework)
- **Axios** (HTTP client)

## System Requirements

### Backend Requirements

- Python 3.8 or higher
- 4 GB RAM minimum
- CUDA 11.8+ (optional, for GPU acceleration)
- macOS or Linux (or Windows with WSL2)

### Frontend Requirements

- Node.js 18 or higher
- NPM 9 or higher

## Installation and Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd Unselected/backend
```

2. Create a Python virtual environment:
```bash
python3 -m venv venv
```

3. Activate the virtual environment:

On macOS/Linux:
```bash
source venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate
```

4. Install Python dependencies:
```bash
pip install -r ../requirements.txt
```

5. Download model weights (required on first run):

The model checkpoint will be downloaded automatically on first inference if not present. Alternatively, download manually:

```bash
mkdir -p checkpoints
curl -L -o checkpoints/depth_anything_v2_vits.pth \
  https://huggingface.co/LiheYoung/depth_anything_v2/resolve/main/depth_anything_v2_vits.pth
```

Model download size: approximately 90 MB

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd Unselected/frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Create environment configuration (optional):

Create a `.env.local` file in the `frontend/` directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

If not specified, the application defaults to `http://localhost:8000/api`.

## Compilation and Execution

### Backend Compilation and Execution

1. Ensure Python virtual environment is activated:
```bash
cd Unselected/backend
source venv/bin/activate  # On macOS/Linux
```

2. Start the FastAPI server:
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

The backend API will be available at:
- Application: http://localhost:8000
- API Documentation: http://localhost:8000/docs (Swagger UI)
- Alternative API Docs: http://localhost:8000/redoc

Success indicators:
- Console output: "Uvicorn running on http://127.0.0.1:8000"
- Swagger UI loads at http://localhost:8000/docs
- Health check returns status "healthy"

### Frontend Compilation and Execution

1. Navigate to frontend directory:
```bash
cd Unselected/frontend
```

2. Start the development server:
```bash
npm run dev
```

The frontend will be available at: http://localhost:3000

Success indicators:
- Console output: "▲ Next.js development server ready"
- Application loads at http://localhost:3000
- Can interact with upload interface

## API Endpoints

### Health and Status

```
GET /api/health
Response: { "status": "healthy", "message": "Image2Surface API is running" }
```

### Image Upload

```
POST /api/image/upload
Content-Type: multipart/form-data
Body: { "file": <image_file> }

Response: {
  "status": "success",
  "image": {
    "imageId": "<uuid>",
    "filename": "<original_filename>",
    "width": <width>,
    "height": <height>
  }
}
```

### Surface Generation

```
POST /api/surface/generate
Content-Type: application/json
Body: {
  "image_id": "<uuid>"
}

Response: {
  "status": "success",
  "mesh": {
    "vertices": [[x, y, z], ...],
    "indices": [[v0, v1, v2], ...]
  }
}
```

### Mesh Editing

```
POST /api/surface/edit
Content-Type: application/json
Body: {
  "image_id": "<uuid>",
  "operation": "smooth|sharpen|scale",
  "intensity": 1.0
}

Response: {
  "status": "success",
  "mesh": {
    "vertices": [[x, y, z], ...],
    "indices": [[v0, v1, v2], ...]
  }
}
```

### Mesh Reset

```
POST /api/surface/reset
Content-Type: application/json
Body: { "image_id": "<uuid>" }

Response: {
  "status": "success",
  "mesh": {
    "vertices": [[x, y, z], ...],
    "indices": [[v0, v1, v2], ...]
  }
}
```

## Testing the System

### Manual Testing

1. Start both backend and frontend servers as described above

2. Verify backend health:
   - Open http://localhost:8000/docs in a browser
   - Click "Try it out" on the GET /api/health endpoint
   - Verify success response

3. Test image upload:
   - Open http://localhost:3000 in a browser
   - Click "Choose Image" and select a test image
   - Verify image appears in preview

4. Test mesh generation:
   - Click "Generate Surface" button
   - Wait for processing to complete
   - Verify 3D mesh appears in viewer

5. Test mesh editing:
   - With generated mesh visible, use dropdown to select operation
   - Adjust intensity slider
   - Click "Apply" and verify mesh updates

6. Test mesh reset:
   - Click "Reset Mesh" button
   - Verify mesh returns to original state

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
lsof -i :8000  # Find process using port
kill -9 <PID>  # Kill the process
```

**Model download fails:**
```bash
# Download manually and place in backend/checkpoints/
# Or check internet connectivity
```

**CUDA/GPU not detected:**
```bash
# Application automatically falls back to CPU
# Performance will be slower but functional
```

### Frontend Issues

**Port 3000 already in use:**
```bash
lsof -i :3000
kill -9 <PID>
```

**Dependencies fail to install:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**API connection fails:**
- Verify backend is running on http://localhost:8000
- Check NEXT_PUBLIC_API_URL environment variable
- Verify CORS is enabled on backend

## Performance Characteristics

- Image upload: < 1 second (limited by network)
- Depth estimation: 2-5 seconds (GPU), 10-20 seconds (CPU)
- Mesh generation: < 1 second
- Mesh editing: < 1 second
- Rendering: 60 FPS on modern hardware

## Workflow

1. **Upload** - Select a PNG/JPG image (max 5MB)
2. **Generate** - AI estimates depth and creates 3D mesh
3. **View** - Interact with the 3D model (rotate, zoom)
4. **Edit** - Apply adjustments:
   - Scale height
   - Smooth surface
   - Sharpen details
5. **Reset** - Return to original mesh state

## Architectural Differences: Selected vs Unselected

### File Organization

**Selected (Layered):**
- `server.py` - All routes in one file, organized by HTTP method
- Direct function calls between layers
- Minimal folder structure for backend

**Unselected (MVC):**
- `controllers/` - Separate files per resource/domain
- `models/` - Domain object definitions
- `services/` - Business logic separated from routing
- Clear separation of concerns by folder

### Request Flow

**Selected (Layered):**
```
Request → FastAPI Route → Processing Function → Infrastructure
```

**Unselected (MVC):**
```
Request → Controller → Service → Model Operations → Infrastructure
```

### Data Handling

**Selected:**
- Data transformed at API boundaries
- Database models optional
- Focus on stateless operations

**Unselected:**
- Domain models carry data and operations
- Models are explicit representations of domain concepts
- Type-safe model instances throughout flow

### Advantages of This (Unselected) Approach

- **Explicit Models**: Domain concepts are represented as first-class objects
- **Coordinated Handling**: Controllers orchestrate complex workflows
- **Reusable Components**: Services can be composed and reused
- **Clear Organization**: Folder structure immediately conveys architecture
- **Self-Documenting**: Code structure mirrors domain understanding

### Trade-offs

- **More Files**: Controllers and services add indirection
- **More Abstractions**: Additional layers of abstraction vs. direct calls
- **Slightly More Complex**: Requires understanding MVC pattern
- **Model Serialization**: Models must be serialized to JSON for responses

## Summary

**Unselected Architecture: Model-View-Controller**

**Advantages:**
- Explicit domain modeling with first-class models
- Coordinated request handling through controllers
- Clear folder structure and organization
- Reusable and composable service layer
- Self-documenting code through structure

**Trade-offs:**
- More files and deeper folder structure
- Additional abstraction layers
- Model-to-JSON serialization needed
- Slightly steeper learning curve for teams unfamiliar with MVC

This architecture is ideal for projects that value explicit domain modeling and organized code structure, especially as the codebase grows in complexity.
