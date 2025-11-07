# ============================================
# main.py - FastAPI Main Application
# ============================================

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
import os
from dotenv import load_dotenv
import asyncio
import openai

load_dotenv()

app = FastAPI(title="Multi-Agent Design System API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Setup
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.multi_agent_design
projects_collection = db.projects

# OpenAI Setup (Optional - for real AI integration)
openai.api_key = os.getenv("OPENAI_API_KEY", "")


# ============================================
# Pydantic Models
# ============================================

class DesignComponent(BaseModel):
    component: str
    structure: str
    styling: str
    reasoning: str

class TechnicalSpecs(BaseModel):
    framework: str
    styling: str
    responsive: bool
    accessibility: str

class Design(BaseModel):
    timestamp: datetime
    designs: List[DesignComponent]
    technical_specs: TechnicalSpecs

class Review(BaseModel):
    timestamp: datetime
    score: int
    status: str
    strengths: List[str]
    issues: List[str]
    suggestions: List[str]

class HumanApproval(BaseModel):
    approved: bool
    feedback: Optional[str] = ""
    timestamp: datetime
    approver: str

class ProjectCreate(BaseModel):
    name: str
    requirements: str

class ProjectResponse(BaseModel):
    id: str
    name: str
    requirements: str
    status: str
    created_at: datetime
    design: Optional[Design] = None
    review: Optional[Review] = None
    human_approval: Optional[HumanApproval] = None

class ApprovalRequest(BaseModel):
    approved: bool
    feedback: Optional[str] = ""


# ============================================
# AI Agent 1: Design Generator
# ============================================

async def ai_agent_1_generate_design(requirements: str) -> Design:
    """
    AI Agent 1: Generates design based on requirements
    Can be replaced with actual OpenAI/Claude API calls
    """
    await asyncio.sleep(2)  # Simulate processing time
    
    # Simulated design generation
    designs = [
        DesignComponent(
            component="Header Component",
            structure="Logo + Navigation Menu + CTA Button + Mobile Hamburger",
            styling="Dark gradient (slate-900 to slate-800), white text, glass morphism effect, sticky positioning",
            reasoning="Modern header with clear visual hierarchy. Sticky positioning ensures constant navigation access. Glass morphism adds premium feel."
        ),
        DesignComponent(
            component="Hero Section",
            structure="Large Heading + Subheading + Hero Image/Video + Dual CTA Buttons + Trust Indicators",
            styling="Full viewport height, gradient background, bold typography (4xl-6xl), animated elements, responsive grid",
            reasoning="Eye-catching hero section designed to immediately capture attention and communicate value proposition. Dual CTAs provide primary and secondary actions."
        ),
        DesignComponent(
            component="Features Grid",
            structure="3-column grid with icon cards, each containing: Icon + Title + Description + Learn More link",
            styling="Card-based layout with shadows, hover lift effect, consistent spacing (gap-6), rounded corners (rounded-xl)",
            reasoning="Scannable layout that highlights key features. Card design allows easy content digestion. Hover effects add interactivity."
        ),
        DesignComponent(
            component="Social Proof Section",
            structure="Customer testimonials carousel + Client logos grid + Statistics counter",
            styling="Alternating background color, contained width, auto-scrolling carousel, fade animations",
            reasoning="Builds trust through social validation. Statistics provide concrete proof of value. Testimonials add human element."
        ),
        DesignComponent(
            component="Footer Component",
            structure="Multi-column layout: Company Info + Quick Links + Resources + Newsletter Signup + Social Links",
            styling="Dark background (slate-900), organized columns, subtle borders, responsive stack on mobile",
            reasoning="Comprehensive footer providing easy access to all important links and information. Newsletter signup captures leads."
        )
    ]
    
    technical_specs = TechnicalSpecs(
        framework="React 18 with TypeScript",
        styling="Tailwind CSS v3 with custom theme extensions",
        responsive=True,
        accessibility="WCAG 2.1 AA compliant with ARIA labels, semantic HTML, keyboard navigation support"
    )
    
    return Design(
        timestamp=datetime.utcnow(),
        designs=designs,
        technical_specs=technical_specs
    )


# ============================================
# AI Agent 2: Design Reviewer
# ============================================

async def ai_agent_2_review_design(design: Design, requirements: str) -> Review:
    """
    AI Agent 2: Reviews the generated design
    Can be replaced with actual AI API calls for sophisticated review
    """
    await asyncio.sleep(2)  # Simulate processing time
    
    score = 85
    issues = []
    suggestions = []
    
    strengths = [
        "Well-structured component hierarchy with clear separation of concerns",
        "Responsive design approach ensures compatibility across all devices",
        "Accessibility considerations properly integrated from the start",
        "Modern visual aesthetic aligned with current design trends",
        "Comprehensive technical specifications provided",
        "Each component has clear reasoning justifying design decisions"
    ]
    
    # Simulate intelligent review
    component_count = len(design.designs)
    
    if component_count < 3:
        issues.append("Limited number of components may not cover all user needs")
        score -= 10
    
    if not design.technical_specs.responsive:
        issues.append("CRITICAL: Design must be responsive for mobile users")
        score -= 20
    
    if "accessibility" not in design.technical_specs.accessibility.lower():
        issues.append("Accessibility standards not clearly defined")
        score -= 15
    
    # Add constructive suggestions
    suggestions.extend([
        "Consider adding loading states and skeleton screens for better perceived performance",
        "Implement micro-animations for improved user engagement and feedback",
        "Add dark mode toggle for user preference accommodation",
        "Include error boundary components for graceful error handling",
        "Consider implementing progressive image loading for performance",
        "Add A/B testing hooks for future optimization",
        "Include analytics tracking for user behavior insights"
    ])
    
    status = "approved" if score >= 80 else "needs_revision"
    
    return Review(
        timestamp=datetime.utcnow(),
        score=score,
        status=status,
        strengths=strengths,
        issues=issues,
        suggestions=suggestions
    )


# ============================================
# Background Task: AI Processing Pipeline
# ============================================

async def process_ai_pipeline(project_id: str, requirements: str):
    """
    Background task that runs the AI pipeline:
    1. AI Agent 1 generates design
    2. AI Agent 2 reviews design
    3. Updates project status
    """
    try:
        # Update status to generating
        await projects_collection.update_one(
            {"_id": ObjectId(project_id)},
            {"$set": {"status": "generating"}}
        )
        
        # AI Agent 1: Generate Design
        design = await ai_agent_1_generate_design(requirements)
        await projects_collection.update_one(
            {"_id": ObjectId(project_id)},
            {
                "$set": {
                    "design": design.dict(),
                    "status": "reviewing"
                }
            }
        )
        
        # AI Agent 2: Review Design
        review = await ai_agent_2_review_design(design, requirements)
        new_status = "pending_approval" if review.status == "approved" else "needs_revision"
        
        await projects_collection.update_one(
            {"_id": ObjectId(project_id)},
            {
                "$set": {
                    "review": review.dict(),
                    "status": new_status
                }
            }
        )
        
    except Exception as e:
        print(f"Error in AI pipeline: {str(e)}")
        await projects_collection.update_one(
            {"_id": ObjectId(project_id)},
            {"$set": {"status": "error", "error_message": str(e)}}
        )


# ============================================
# API Routes
# ============================================

@app.get("/")
async def root():
    return {
        "message": "Multi-Agent Design System API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "database": "connected" if client else "disconnected"
    }


@app.post("/api/projects", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, background_tasks: BackgroundTasks):
    """
    Create a new project and trigger AI processing pipeline
    """
    project_data = {
        "name": project.name,
        "requirements": project.requirements,
        "status": "pending",
        "created_at": datetime.utcnow(),
        "design": None,
        "review": None,
        "human_approval": None
    }
    
    result = await projects_collection.insert_one(project_data)
    project_id = str(result.inserted_id)
    
    # Trigger AI pipeline in background
    background_tasks.add_task(process_ai_pipeline, project_id, project.requirements)
    
    project_data["id"] = project_id
    return ProjectResponse(**project_data)


@app.get("/api/projects", response_model=List[ProjectResponse])
async def get_all_projects(skip: int = 0, limit: int = 100):
    """
    Get all projects with pagination
    """
    cursor = projects_collection.find().sort("created_at", -1).skip(skip).limit(limit)
    projects = await cursor.to_list(length=limit)
    
    result = []
    for project in projects:
        project["id"] = str(project.pop("_id"))
        result.append(ProjectResponse(**project))
    
    return result


@app.get("/api/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """
    Get a specific project by ID
    """
    try:
        project = await projects_collection.find_one({"_id": ObjectId(project_id)})
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        project["id"] = str(project.pop("_id"))
        return ProjectResponse(**project)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/projects/{project_id}/approve")
async def approve_project(project_id: str, approval: ApprovalRequest):
    """
    Human approval/rejection of a project
    """
    try:
        project = await projects_collection.find_one({"_id": ObjectId(project_id)})
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        if project["status"] != "pending_approval":
            raise HTTPException(
                status_code=400, 
                detail=f"Project cannot be approved in current status: {project['status']}"
            )
        
        human_approval = HumanApproval(
            approved=approval.approved,
            feedback=approval.feedback or "",
            timestamp=datetime.utcnow(),
            approver="Human Reviewer"
        )
        
        new_status = "approved" if approval.approved else "rejected"
        
        await projects_collection.update_one(
            {"_id": ObjectId(project_id)},
            {
                "$set": {
                    "human_approval": human_approval.dict(),
                    "status": new_status
                }
            }
        )
        
        return {"message": f"Project {new_status}", "project_id": project_id}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: str):
    """
    Delete a project
    """
    try:
        result = await projects_collection.delete_one({"_id": ObjectId(project_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return {"message": "Project deleted successfully", "project_id": project_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/projects/{project_id}/regenerate")
async def regenerate_design(project_id: str, background_tasks: BackgroundTasks):
    """
    Regenerate design for a project (restart AI pipeline)
    """
    try:
        project = await projects_collection.find_one({"_id": ObjectId(project_id)})
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Reset project status
        await projects_collection.update_one(
            {"_id": ObjectId(project_id)},
            {
                "$set": {
                    "status": "pending",
                    "design": None,
                    "review": None,
                    "human_approval": None
                }
            }
        )
        
        # Trigger AI pipeline again
        background_tasks.add_task(process_ai_pipeline, project_id, project["requirements"])
        
        return {"message": "Design regeneration started", "project_id": project_id}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/stats")
async def get_statistics():
    """
    Get system statistics
    """
    total_projects = await projects_collection.count_documents({})
    pending = await projects_collection.count_documents({"status": "pending_approval"})
    approved = await projects_collection.count_documents({"status": "approved"})
    rejected = await projects_collection.count_documents({"status": "rejected"})
    
    return {
        "total_projects": total_projects,
        "pending_approval": pending,
        "approved": approved,
        "rejected": rejected,
        "timestamp": datetime.utcnow()
    }


# ============================================
# Run with: uvicorn main:app --reload
# ============================================