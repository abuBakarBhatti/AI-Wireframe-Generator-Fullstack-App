export interface WireframeResponse {
    svg_code: string;
    detailed_requirements?: Record<string, any>;
    wireframe_plan?: Record<string, any>;
    errors?: string[];
}

