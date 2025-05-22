from typing import List, Dict, Any, Optional
from app.utils.text_processing import clean_svg, extract_json_from_text, extract_svg_from_text, parse_json_safely
from app.config import Settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
import json

from app.models.wireframe import WireframeState

from app.config import settings 




def get_llm_model(TEMPERATURE: float = 0):
    """" Get llm model with configured settings """

    return ChatGoogleGenerativeAI(
        model=settings.DEFAULT_MODEL,
        api_key=settings.GOOGLE_API_KEY,
        temperature=TEMPERATURE,
        max_tokens=None,
        timeout=None,
        max_retries=3,
    )


@traceable
def query_expansion_agent(state: WireframeState) -> WireframeState:
    """
    Expand and refine the user query to provide more context and details
    
    Args:
        state: The current state containing the raw user_query
        
    Returns:
        Updated state with expanded_query and original_query
    """
    raw_query = state["user_query"]
    
    prompt = f"""
    ### Task:
    You are interpreting a user's wireframe request to make it clearer for processing. Your goal is to restructure the query for better comprehension WITHOUT adding new information or removing any specifications provided by the user.
    
    ### Original Request:
    "{raw_query}"
    
    ### Instructions:
    1. Preserve ALL technical specifications exactly as provided (dimensions, components, layout details)
    2. Preserve ALL functional requirements mentioned by the user
    3. Preserve ALL style/design preferences mentioned by the user
    4. Reorganize information in a logical structure if needed (e.g., group by page/component)
    5. Fix any unclear phrasing or ambiguous language
    6. Do NOT add any new features, pages, or requirements not explicitly mentioned
    7. Do NOT remove any details provided by the user, no matter how minor
    8. Do NOT make assumptions about user needs beyond what's stated
    9. Don't say like this way " the user has requested this ......" rather you should use words like "I want to have this or I want to create this ...... etc"
    
    ### Response Format:
    Return only a JSON object:
    ```json
    {{
        "interpreted_query": "Your restructured query here"
    }}
    ```
    """
    
    model = get_llm_model()
    response = model.invoke(prompt)
    
    try:
        # Extract JSON from the response
        json_content = extract_json_from_text(response.content)
        expansion_result = parse_json_safely(json_content)
        expanded_query = expansion_result.get("interpreted_query", raw_query)
        
        # Add the expanded query to the state, keeping the original for reference
        return {
            **state,
            "original_query": raw_query,
            "user_query": expanded_query,
        }
    except Exception as e:
        return {
            **state,
            "errors": (state.get("errors") or []) + [f"Error in query expansion: {str(e)}"]
        }



# requrement gathering agent
@traceable
def requirement_gathering_agent(state: WireframeState) -> WireframeState:
    """" 
    Get requirement gathered from user query 
    
    Args:
        state: The current state containing user_query
        
    Returns:
        Updated state with detailed_requirements
    """

    user_query = state["user_query"]

#     prompt = f"""  
#             ### Introduction:
# You are an expert requirements gathering agent for a wireframe generator. Your role is to analyze user requests and extract detailed specifications needed to create appropriate wireframes.

# ### Context:
# The user has requested: "{user_query}"

# ### Instructions:
# 1. **Understand the Core Request:**
#    - What type of website/application is being requested? 
#    - What is its primary purpose?
#    - What kind of desing preferences does the user have?
#    - What kind of modernity level does the user want? 
#    - etc etc 

# 2. **Identify Explicit Requirements:**
#    - What specific features, pages, or design elements has the user explicitly mentioned?

# 3. **Recognize Implicit Needs:**
#    - Based on the website type and purpose, what standard features would be expected?

# 4. **Consider the Target Audience:**
#    - Who will use this website and what are their likely expectations?

# 5. **Evaluate Design Preferences:**
#    - Has the user specified fidelity level, style, or specific visual elements?

# 6. **Identify Information Gaps:**
#    - What important details are missing that you need to make reasonable assumptions about?

# 7. **Apply Industry Standards:**
#    - What common patterns and best practices apply to this type of website/application?

# ### Output Requirements:
# Please analyze this request thoroughly and extract comprehensive requirements. If certain details are missing but can be reasonably inferred from the context or industry standards, make appropriate assumptions while noting them explicitly.

# Your response should include the following detailed requirements:

# 1. **Project Type and Purpose:**
#    - Type of website/application (e.g., e-commerce, portfolio, blog, corporate)
#    - Primary purpose and business objectives
#    - Industry/sector

# 2. **Target Audience:**
#    - Demographics (age range, technical proficiency)
#    - User personas and their goals
#    - Accessibility considerations

# 3. **Visual and Design Preferences:**
#    - Desired wireframe fidelity level (low, medium, high)
#    - Style preferences (modern, minimalist, corporate, etc.)
#    - Brand elements to incorporate (logo, colors, etc.)
#    - Layout preferences (responsive, fixed-width)

# 4. **Features and Functionality:**
#    - Primary user interactions
#    - Core functionality
#    - Navigation structure
#    - Authentication requirements (if any)

# 5. **Content Structure:**
#    - Required pages and their hierarchy
#    - Key sections per page
#    - Content blocks (text, images, forms, etc.)
#    - Call-to-actions

# 6. **Technical Considerations:**
#    - Device compatibility requirements
#    - Special technical requirements

# 7. **Assumptions and Reasoning:**
#    - List any assumptions you made and why
#    - Confidence level in your interpretations

# ### Output Format:
# - Format your response as structured JSON that can be parsed by the next agent.
# - Include a `confidence_level` property (low/medium/high) for each inferred requirement to indicate certainty.

# ### Final Review:
# Before finalizing, review your output and ensure:
# 1. All critical aspects of the request have been addressed.
# 2. The requirements are consistent with the type of website/application.
# 3. The detail level is appropriate for the specified fidelity.
# 4. All assumptions are reasonable and clearly marked.

# """

    prompt = f"""
          ### Introduction:
You are an expert requirements gathering agent for a wireframe generator. Your role is to analyze user requests and extract detailed specifications needed to create appropriate wireframes.

### Context:
The user has requested: "{user_query}"

### Instructions:
1. **Understand the Core Request:**
   - What type of website/application is being requested?
   - What is its primary purpose?
   - What specific problem is it solving for end users?
   - What business goals does it serve?

2. **Identify User Experience Needs:**
   - What key user journeys should be supported?
   - What critical task flows must be included?
   - What content types will users engage with most?
   - What key decisions will users make while using this product?

3. **Identify Explicit Requirements:**
   - What specific features, pages, or design elements has the user explicitly mentioned?
   - What functional capabilities are directly requested?
   - Are there any explicit design preferences mentioned?

4. **Recognize Implicit Needs:**
   - Based on the website type and purpose, what standard features would be expected?
   - What common components are industry-standard for this type of product?
   - What content structures are typically needed to support the stated purpose?

5. **Consider the Target Audience:**
   - Who will use this website/application (demographics, technical proficiency)?
   - What are their primary goals and pain points?
   - What devices and contexts will they likely use this in?
   - What accessibility considerations are relevant?

6. **Evaluate Design Preferences:**
   - What level of visual fidelity is appropriate?
   - What aesthetic style aligns with the brand and audience (modern, corporate, playful, etc.)?
   - Are there color preferences or brand guidelines mentioned?
   - What content-to-whitespace ratio would be appropriate?

7. **Identify Information Gaps:**
   - What critical information is missing that requires assumptions?
   - What requirements would significantly change based on missing information?

8. **Apply Industry Standards and Best Practices:**
   - What common patterns apply to this type of website/application?
   - What usability principles are most relevant?
   - Are there regulatory or compliance considerations?

### Output Requirements:
Please analyze this request thoroughly and extract comprehensive requirements. If certain details are missing but can be reasonably inferred from the context or industry standards, make appropriate assumptions while noting them explicitly.

Your response should include the following detailed requirements:

1. **Project Type and Purpose:**
   - Type of website/application (e.g., e-commerce, portfolio, blog, corporate)
   - Primary purpose and business objectives
   - Industry/sector
   - Key performance indicators

2. **Target Audience:**
   - Demographics (age range, technical proficiency)
   - User personas and their goals
   - User contexts and environments
   - Accessibility considerations

3. **User Journeys and Tasks:**
   - Primary user flows
   - Critical tasks to support
   - Content discovery patterns
   - Decision points and user needs at each stage

4. **Visual and Design Preferences:**
   - Desired wireframe fidelity level (low, medium, high)
   - Style preferences (modern, minimalist, corporate, etc.)
   - Brand elements to incorporate (logo, colors, etc.)
   - Content density and whitespace approach
   - Visual hierarchy priorities

5. **Features and Functionality:**
   - Primary user interactions
   - Core functionality requirements
   - Navigation structure and patterns
   - Search and filtering capabilities
   - Authentication requirements (if any)
   - Social or sharing features

6. **Content Structure:**
   - Required pages and their hierarchy
   - Key sections per page
   - Content blocks (text, images, forms, etc.)
   - Call-to-actions
   - Content prioritization

7. **Technical Considerations:**
   - Device compatibility requirements
   - Responsive design breakpoints
   - Performance considerations
   - Special technical requirements

8. **Assumptions and Reasoning:**
   - List any assumptions you made and why
   - Confidence level in your interpretations
   - Alternative interpretations considered

### Output Format:
- Format your response as structured JSON that can be parsed by the next agent.
- Include a `confidence_level` property (low/medium/high) for each inferred requirement to indicate certainty.
- Include a `priority` property (critical/high/medium/low) for each requirement.

### Final Review:
Before finalizing, review your output and ensure:
1. All critical aspects of the request have been addressed.
2. The requirements are consistent with the type of website/application.
3. The detail level is appropriate for the specified fidelity.
4. All assumptions are reasonable and clearly marked.
5. The requirements support a cohesive user experience. """
    
    model = get_llm_model(TEMPERATURE=settings.MODEL_TEMPERATURE)

    response = model.invoke(prompt)

    try:
        # Extract JSON from the response
        json_content = extract_json_from_text(response.content)
        detailed_requirements = parse_json_safely(json_content)

        # Add the detailed requirements to the state
        return {
            **state,
            "detailed_requirements": detailed_requirements,
        }
    except Exception as e:
        return {
            **state,
            "errors": (state.get("errors") or []) + [f"Error in requirements gathering: {str(e)}"]
        }


# wireframe planning agent
@traceable
def wireframe_planning_agent(state: WireframeState) -> WireframeState:
    """
        Agent for translating detailed requirements into a wireframe plan.
    
        Args:
            state: The current state containing detailed_requirements
        
        Returns:
            Updated state with wireframe_plan
    """

    detailed_requirements = state['detailed_requirements']
    
    # Convert requirements to JSON string for the prompt (for model better readability)
    requirements_json = json.dumps(detailed_requirements, indent=2)

    prompt = f"""
### Introduction:
You are an expert wireframe planning agent specializing in translating project requirements into detailed wireframe specifications. Your expertise spans UX design principles, user flow optimization, information architecture, and visual hierarchy implementation.

### Context:
Based on these detailed requirements:
{requirements_json}

### Chain of Thought Process:
You will think through this wireframe planning process step by step, documenting your reasoning at each stage. For each decision point, articulate:

1. **What options you considered**
2. **Why you selected specific approaches**
3. **How this connects to user needs and project goals**
4. **What trade-offs you're making**

### Instructions:

1. **Requirements Analysis & Prioritization:**
   - THINKING STEP: Categorize requirements into "must-have," "should-have," and "nice-to-have" based on user impact and core functionality.
   - THINKING STEP: Identify any unstated but necessary components that should be included based on standard practices.
   - THINKING STEP: Note any conflicts or tensions between different requirements that need resolution.
   - OUTPUT: Produce a prioritized list of requirements with rationale for prioritization.

2. **User Persona & Journey Mapping:**
   - THINKING STEP: Based on requirements, infer the primary and secondary user personas.
   - THINKING STEP: For each persona, map their mental model and expectations when approaching this interface.
   - THINKING STEP: Identify the emotional and functional needs at each journey stage.
   - OUTPUT: Define 2-3 key user personas and their primary journeys through the application.

3. **Information Architecture Development:**
   - THINKING STEP: Consider multiple organizational schemes (hierarchical, sequential, matrix, etc.) and their appropriateness.
   - THINKING STEP: Evaluate navigation patterns based on content complexity and user familiarity.
   - THINKING STEP: Assess content relationships and natural groupings.
   - OUTPUT: Detailed sitemap with hierarchy, relationships, and navigation patterns justified by user needs.

4. **User Flow Optimization:**
   - THINKING STEP: Map primary, secondary, and edge-case user paths through the interface.
   - THINKING STEP: Identify potential friction points and their solutions.
   - THINKING STEP: Consider where users might get lost and how to prevent it.
   - OUTPUT: Comprehensive user flow diagrams with decision points and path optimizations.

5. **Screen Layout Design:**
   - THINKING STEP: For each screen, consider content prioritization based on user goals and business objectives.
   - THINKING STEP: Apply suitable grid systems based on content type and device considerations.
   - THINKING STEP: Apply visual hierarchy principles to guide attention appropriately.
   - THINKING STEP: Consider how layout supports scanning patterns (F-pattern, Z-pattern, etc.).
   - OUTPUT: Layout specifications with grid definitions, content blocks, and hierarchy justifications.

6. **UI Component Selection:**
   - THINKING STEP: For each interaction need, evaluate different component options.
   - THINKING STEP: Consider component familiarity vs. innovation needs.
   - THINKING STEP: Assess accessibility implications of component choices.
   - THINKING STEP: Plan for component states and variations.
   - OUTPUT: Component inventory with justifications, states, and usage guidelines.

7. **Fidelity Level Implementation:**
   - THINKING STEP: Based on project requirements, determine appropriate fidelity for different elements.
   - THINKING STEP: Decide where higher fidelity details add value vs. where they might distract.
   - OUTPUT: Fidelity specifications for different wireframe elements with rationale.

8. **Responsiveness & Adaptivity Planning:**
   - THINKING STEP: Identify how layouts will transform across breakpoints.
   - THINKING STEP: Determine component behavior changes for different devices.
   - THINKING STEP: Consider touch vs. pointer input differences.
   - OUTPUT: Responsive strategy with breakpoint specifications and component adaptations.

9. **Review & Refinement:**
   - THINKING STEP: Evaluate the entire plan against original requirements.
   - THINKING STEP: Check for consistency in patterns, terminology, and interactions.
   - THINKING STEP: Identify any areas where simplification would benefit users.
   - OUTPUT: List of refinements applied and their justifications.

### Deliverables:
Create a comprehensive wireframe plan that balances usability, aesthetics, and functionality while documenting your reasoning process. Your plan should include:

1. **Strategic Overview:**
   - Project goals and target users
   - Key design principles being applied
   - Overall approach and rationale
   - Critical success metrics for the wireframes

2. **Information Architecture:**
   - Complete sitemap with all screens/pages and clear hierarchy
   - Navigation structure and content organization schemas
   - Taxonomies and labeling systems
   - Relationship diagrams between content areas

3. **User Journey Maps:**
   - Primary user flows with annotated touchpoints
   - Entry and exit points with context
   - Success and failure paths
   - Conversion funnels and optimization points

4. **Screen Specifications:**
   - For each screen:
     - Purpose and user objectives
     - Content priority matrix
     - Interaction model and behavior
     - Layout specification with zones and proportions
     - Component placement with rationale
     - States and variations
     - Responsive behavior specifications

5. **Component Library Planning:**
   - Reusable UI patterns and components
   - State definitions and transitions
   - Modularity and composition rules
   - Typography and iconography usage

6. **Design System Elements:**
   - Grid specifications and spacing systems
   - Alignment and proportion guidelines
   - Layout patterns and their applications
   - Consistency measures across screens

7. **Technical Considerations:**
   - SVG implementation guidance
   - Interactive element specifications
   - Performance considerations
   - Accessibility requirements

8. **Annotated Wireframe Plan:**
   - Key decisions and their rationales
   - Alternative approaches considered
   - Usability considerations
   - Future iteration recommendations

### Fidelity Level Guide:
Include specifications on wireframe fidelity using this framework:

1. **Low Fidelity** - Structural only: basic shapes, no detailed UI elements, focus on layout and flow
2. **Medium Fidelity** - Representative UI elements: distinguishable components, limited detail, focus on interaction and placement
3. **High Fidelity** - Detailed UI: specific components with states, proportionally accurate, includes some visual design elements
4. **Production Fidelity** - Implementation ready: precise specifications, component variants, includes aesthetic details

### Output Format:
- Format your response as structured JSON that can be easily parsed by the SVG generator agent.
- Output a valid JSON object only. Do NOT include comments like this '//' or trailing commas. Wrap your response in a ```json code block.
- Use descriptive keys and nested structures to clearly organize the wireframe plan.
- Include a "reasoning" field for each major decision to document your chain of thought.

      ### JSON Structure Guide:
      ``` json
      {{
      "metadata": {{
         "project_name": "",
         "fidelity_level": "",
         "target_devices": [],
         "design_approach": ""
      }},
      "strategic_overview": {{
         "goals": [],
         "target_users": [],
         "design_principles": [],
         "key_metrics": [],
         "reasoning": ""
      }},
      "information_architecture": {{
         "sitemap": [],
         "navigation": {{}},
         "content_organization": {{}},
         "reasoning": ""
      }},
      "user_journeys": [],
      "screens": [
         {{
            "id": "",
            "name": "",
            "purpose": "",
            "content_priority": {{}},
            "layout": {{}},
            "components": [],
            "states": [],
            "responsive_behavior": {{}},
            "reasoning": ""
         }}
      ],
      "component_library": [],
      "design_system": {{}},
      "technical_considerations": {{}},
      "annotations": {{}}
      }} 

   ``` 

### Guidelines:

Validation Checklist:
Before finalizing, validate your plan against these criteria:

1.Does each screen have a clear purpose aligned with user goals?
2.Is the navigation intuitive and consistent?
3.Does the information architecture support user mental models?
4.Are all required functionalities addressed?
5. Is the fidelity level appropriate and consistent?
6.Is the chain of thought reasoning documented for key decisions?
7.Do the specifications provide sufficient detail for SVG generation?
8. Does the plan balance innovation with usability conventions?
9.Are accessibility considerations integrated throughout?
10. Does the overall approach align with project requirements and constraints?

Remember to justify and document your thinking at each step, making your chain of thought explicit in the JSON output.
"""

#     prompt = f"""  ### Introduction:
# You are an expert wireframe planning agent for translating project requirements into detailed wireframe specifications. Your expertise spans UX design principles, user flow optimization, and information architecture.

# ### Context:
# Based on these detailed requirements:
# {requirements_json}

# ### Instructions:
# 1. **Analyze the Requirements:**
#    - Review all requirements thoroughly to understand the project scope, goals, and constraints.

# 2. **Define the Information Architecture:**
#    - Identify all necessary screens/pages based on explicit requirements and standard practices.
#    - Establish logical hierarchy and grouping of pages.
#    - Determine primary, secondary, and tertiary navigation patterns.
#    - Map relationships between different screens.

# 3. **Plan the User Flows:**
#    - Identify entry points and key user journeys.
#    - Map primary paths users will take to accomplish core tasks.
#    - Consider edge cases and alternative flows.
#    - Define transitions and connections between screens.

# 4. **Design Screen Layouts:**
#    - Determine appropriate grid system and breakpoints based on requirements.
#    - Allocate space for key content blocks according to priority and hierarchy.
#    - Position critical UI elements based on usability principles and visual hierarchy.
#    - Ensure consistent layout patterns across similar screens.

# 5. **Specify UI Components:**
#    - Identify all necessary UI components for each screen.
#    - Determine states and variations of interactive components.
#    - Define reusable component patterns for consistency.
#    - Consider appropriate component fidelity based on requirements.

# 6. **Review and Refine:**
#    - Evaluate if the plan addresses all requirements.
#    - Check for usability issues or flow problems.
#    - Ensure consistency across the wireframe plan.
#    - Verify that the fidelity level matches requirements.

# ### Deliverables:
# Create a comprehensive wireframe plan that balances usability, aesthetics, and functionality. Pay special attention to the requested fidelity level and design preferences.

# Your wireframe plan should include:

# 1. **Information Architecture:**
#    - Complete sitemap listing all screens/pages with clear hierarchy.
#    - Logical grouping of pages by function or user journey.
#    - Navigation structure and relationships between pages.

# 2. **Detailed Screen Specifications:**
#    - For each screen/page:
#      - Screen purpose and primary user goals.
#      - Content priority (hierarchy of information).
#      - Key UI components with approximate positioning and sizing.
#      - Interactive elements (buttons, forms, menus, etc.).
#      - Responsive behavior considerations (if applicable).

# 3. **User Flow Mapping:**
#    - Primary user journeys through the interface.
#    - Entry and exit points for key tasks.
#    - Critical paths for core functionality.
#    - Decision points and conditional flows.

# 4. **Layout Framework:**
#    - Grid system specifications.
#    - Consistent spacing and alignment principles.
#    - Header/footer/sidebar treatments.
#    - Content zoning for each page template.

# 5. **Component Specifications:**
#    - Reusable UI components that appear across multiple screens.
#    - State variations for interactive elements.
#    - Annotations for complex interactions.

# 6. **Technical Implementation Notes:**
#    - Any special considerations for the SVG generator.
#    - Adaptive/responsive design breakpoints (if applicable).

# 7. **Design Rationale:**
#    - Explanation of key design decisions and their alignment with requirements.
#    - Notes on how user needs are addressed through the design.

# ### Output Format:
# - Format your response as structured JSON that can be easily parsed by the SVG generator agent.
# - Output a valid JSON object only. Do NOT include comments like this '//' or trailing commas. Wrap your response in a ```json code block.
# - Use descriptive keys and nested structures to clearly organize the wireframe plan.
# - Include metadata about the fidelity level and design approach to guide the visual implementation.

# ### Validation:
# Before finalizing, validate your plan against the requirements to ensure:
# 1. All required screens and functionalities are included.
# 2. The proposed structure supports the stated user goals.
# 3. The fidelity level matches what was requested.
# 4. The plan provides sufficient detail for SVG generation.

# """ 
    


#     prompt = f""" 
#     ### Introduction:
# You are an expert wireframe planning agent for translating project requirements into detailed wireframe specifications. Your expertise spans UX design principles, user flow optimization, information architecture, and creating layouts that prioritize readability and visual comfort.

# ### Context:
# Based on these detailed requirements:
# {requirements_json}

# ### Instructions:
# **0. Guiding Principle: Prioritize Clarity, Readability, and Visual Comfort.**
#    - Throughout the planning process, aim for layouts that are easy to scan, understand, and interact with. Avoid overly dense or "shrunk" presentations. Ensure sufficient whitespace and clear visual separation between elements.

# 1. **Analyze the Requirements:**
#    - Review all requirements thoroughly to understand the project scope, goals, and constraints, paying special attention to any explicit or implicit needs for visual hierarchy and uncluttered interfaces.

# 2. **Define the Information Architecture:**
#    - Identify all necessary screens/pages based on explicit requirements and standard practices.
#    - Establish logical hierarchy and grouping of pages.
#    - Determine primary, secondary, and tertiary navigation patterns.
#    - Map relationships between different screens, considering the need for clear visual transitions and separation.

# 3. **Plan the User Flows:**
#    - Identify entry points and key user journeys.
#    - Map primary paths users will take to accomplish core tasks.
#    - Consider edge cases and alternative flows.
#    - Define transitions and connections between screens.

# 4. **Design Screen Layouts:**
#    - Determine appropriate grid system and breakpoints based on requirements.
#    - **Allocate generous space** for key content blocks according to priority and hierarchy, ensuring adequate **whitespace (breathing room)** around and within them.
#    - Position critical UI elements based on usability principles and visual hierarchy, ensuring that **sufficient spacing is maintained to prevent visual clutter and overlap.** For example, labels should be clearly distinct from their corresponding input fields.
#    - Ensure consistent layout patterns across similar screens, including consistent application of spacing rules.

# 5. **Specify UI Components:**
#    - Identify all necessary UI components for each screen (e.g., buttons, text inputs, cards, modals).
#    - Determine states and variations of interactive components.
#    - Define reusable component patterns for consistency.
#    - Consider appropriate component fidelity based on requirements.
#    - **Crucially, ensure that component specifications include dimensions that allow for adequate internal padding for their content (e.g., text within buttons, content within cards).**

# 6. **Review and Refine:**
#    - Evaluate if the plan addresses all requirements.
#    - Check for usability issues, flow problems, **and potential areas of visual clutter or insufficient spacing.**
#    - Ensure consistency across the wireframe plan, especially in the application of layout and spacing principles.
#    - Verify that the fidelity level matches requirements.

# ### Deliverables:
# Create a comprehensive wireframe plan that balances usability, aesthetics, and functionality. Pay special attention to the requested fidelity level, design preferences, **and the principles of readability and visual comfort outlined above.**

# Your wireframe plan should include:

# 1. **Information Architecture:**
#    - Complete sitemap listing all screens/pages with clear hierarchy.
#    - Logical grouping of pages by function or user journey.
#    - Navigation structure and relationships between pages.

# 2. **Detailed Screen Specifications:**
#    - For each screen/page:
#      - Screen purpose and primary user goals.
#      - Content priority (hierarchy of information).
#      - Key UI components with **explicit approximate positioning and sizing. Sizing must account for content (e.g., text length) and necessary internal padding (e.g., a button's height should comfortably accommodate its text label with clear vertical padding).**
#      - Interactive elements (buttons, forms, menus, etc.) with details on spacing relative to adjacent elements.
#      - Responsive behavior considerations (if applicable).

# 3. **User Flow Mapping:**
#    - Primary user journeys through the interface.
#    - Entry and exit points for key tasks.
#    - Critical paths for core functionality.
#    - Decision points and conditional flows.

# 4. **Layout Framework (Crucial for Avoiding Shrunk Content):**
#    - Grid system specifications (e.g., columns, rows, gutter sizes).
#    - **Explicit Spacing System/Principles:**
#      - Define a base spacing unit (e.g., 8px).
#      - Specify multiples of this unit for common layout needs (e.g., `small: 8px`, `medium: 16px`, `large: 24px`, `xlarge: 32px`).
#      - Provide guidelines or explicit values for:
#        - Margins between major sections.
#        - Padding within container elements (e.g., cards, modals, content blocks).
#        - Spacing between list items or repeated elements.
#        - Vertical rhythm or spacing between paragraphs of text.
#        - Spacing between form labels and their input fields.
#    - Consistent alignment principles.
#    - Header/footer/sidebar treatments, including their internal padding and margins.
#    - Content zoning for each page template, **specifying padding within zones and margins between zones.**

# 5. **Component Specifications:**
#    - Reusable UI components that appear across multiple screens.
#    - State variations for interactive elements.
#    - Annotations for complex interactions.
#    - **For each component, specify or reference the standard internal padding values (from the Layout Framework) to be used.**

# 6. **Technical Implementation Notes:**
#    - Any special considerations for the SVG generator, **particularly regarding how it should interpret and apply the specified spacing system.**
#    - Adaptive/responsive design breakpoints (if applicable).

# 7. **Design Rationale:**
#    - Explanation of key design decisions and their alignment with requirements.
#    - Notes on how user needs, **including the need for a clear and uncluttered interface,** are addressed through the design.

# ### Output Format:
# - Format your response as structured JSON that can be easily parsed by the SVG generator agent.
# - Output a valid JSON object only. Do NOT include comments like this '//' or trailing commas. Wrap your response in a ```json code block.
# - Use descriptive keys and nested structures to clearly organize the wireframe plan.
# - **Ensure the JSON includes specific fields for the defined spacing system/principles (e.g., within a `layoutFramework.spacing` object) so the SVG generator can directly use these values.**
# - Include metadata about the fidelity level and design approach to guide the visual implementation.

# ### Validation:
# Before finalizing, validate your plan against the requirements to ensure:
# 1. All required screens and functionalities are included.
# 2. The proposed structure supports the stated user goals.
# 3. The fidelity level matches what was requested.
# 4. The plan provides sufficient detail for SVG generation, **including explicit spacing and sizing information to prevent dense or overlapping layouts.**
# 5. **The plan actively promotes readability and visual comfort through appropriate use of whitespace and element separation.**
# """


    model = get_llm_model()

    response = model.invoke(prompt)
   #  print("Wireframe planning agent response", response.content)

    try:
        # Extract JSON from the response
        json_content = extract_json_from_text(response.content)
        wireframe_plan = parse_json_safely(json_content)

        # Add the wireframe plan to the state
        return {
            **state,
            "wireframe_plan": wireframe_plan,
        }
    except Exception as e:
        return {
            **state,
            "errors": (state.get("errors") or []) + [f"Error in wireframe planning: {str(e)}"]
        }


# svg generation agent
@traceable
def svg_generator_agent(state: WireframeState) -> WireframeState:
    """
        Agent for generating SVG wireframe based on wireframe plan.
    
        Args:
            state: The current state containing wireframe_plan
        
        Returns:
            Updated state with svg_code
    """

    wireframe_plan = state['wireframe_plan']

    # Convert plan to JSON string for the prompt (for model better readability)
    plan_json = json.dumps(wireframe_plan, indent=2)

    detailed_requirements = state['detailed_requirements']
   


    # Convert requirements to JSON string for the prompt (for model better readability)
   #  requirements_json = json.dumps(detailed_requirements, indent=2)


    prompt = f""" ### Introduction:
You are an expert SVG wireframe generator specializing in translating wireframe plans into clean, semantic SVG code. Your expertise covers visual design principles, SVG optimization, and creating wireframes at various fidelity levels (low, medium, high).

### Context:
Based on this wireframe plan:
{plan_json}

### Instructions:
1. **Analyze the Wireframe Plan:**
   - Identify all screens/pages that need to be created.
   - Understand the relationships and flows between screens.
   - Note the required fidelity level (low, medium, high).
   - Review any specific style requirements or brand elements.

2. **Plan the SVG Structure:**
   - Determine appropriate viewBox dimensions to accommodate all content (e.g., 360x800 for mobile).
   - Plan logical positioning of screens with clear separation.
   - Define a consistent coordinate system (0,0 at top left).
   - Establish proper spacing between screens (minimum 50px).

3. **Design the Styling System:**
   - Create a comprehensive style section with classes for common elements.
   - Define appropriate visual characteristics for the specified fidelity level.
   - Establish color scheme, stroke weights, and fill styles.
   - Ensure sufficient contrast and visual hierarchy.

4. **Implement Each Screen Methodically:**
   - Start with container and layout elements.
   - Add primary content blocks following the specified hierarchy.
   - Implement interactive elements (buttons, forms, menus).
   - Add text elements with appropriate placeholder content.
   - Include navigation components as specified.

5. **Prevent Element Overlapping:**
   - Use ONLY ONE visual representation per element (text OR icon OR symbol).
   - Ensure text labels are positioned separately from visual indicators.
   - Apply proper spacing between elements (minimum 5px).
   - Test for potential overlaps visually before finalizing.

6. **Review and Optimize:**
   - Check that all screens match their specifications.
   - Verify all components are properly positioned and sized.
   - Ensure consistent styling across similar elements.
   - Optimize SVG code for cleanliness and efficiency.

### Wireframe Requirements:

#### Fidelity Implementation:
- **Low-fidelity:** Use basic shapes, simple outlines, minimal text labels, and placeholder blocks.
- **Medium-fidelity:** Add more defined UI components, basic iconography, text hierarchy, and grid structure.
- **High-fidelity:** Include detailed components, proper spacing, realistic proportions, and visual hierarchy indicators.

#### Core Styling Elements:
1. **Define a comprehensive style section with classes for:**
   - `.screen` - Container for each screen (with subtle border).
   - `.screen-header` - Header section for each screen.
   - `.screen-title` - Title text for each screen.
   - `.form-field` - Input field containers.
   - `.form-label` - Text labels for form fields.
   - `.button` - Action buttons with appropriate styling for fidelity level.
   - `.button-label` - Text inside buttons.
   - `.notification` - Success/error message containers.
   - `.navbar` - Navigation bar styling.
   - `.footer` - Footer section styling.
   - `.content-block` - Generic content containers.
   - `.arrow` - Connection lines between screens.
   - `.link-text` - Hyperlinks or navigation text.

#### Element Representation and Clarity:
- **For icon placeholders:** Use EITHER a text label OR a simple shape/symbol, NEVER both overlapping.
- **For navigation items:** Place text labels BELOW or BESIDE icon placeholders with adequate spacing.
- **For interactive elements:** Use consistent visual indicators that don't interfere with text.
- **Maintain clear visual separation between different components.**

#### Technical Specifications:
- Create responsive SVGs with the `viewBox` attribute set appropriately (e.g., `viewBox="0 0 360 800"` for mobile).
- Use `width` and `height` attributes set to 100% for responsive scaling.
- Include proper namespacing and DOCTYPE declarations.
- Use semantic grouping (`<g>` elements) with descriptive ids for logical sections.

#### Layout & Organization:
1. **Position screens in a logical flow.**
2. **Include proper margins between screens (at least 50px).**
3. **Use consistent sizing for similar components.**
4. **Group related elements together using `<g>` tags with descriptive ids.**
5. **Maintain a minimum spacing of 5px between adjacent elements.**

#### Arrow and Flow Representation:
1. **For screen flow connections:**
   - Use SVG `<path>` elements with proper markers for arrows.
   - Implement arrows with a clear direction indicating user flow.
   - Use the following pattern for arrows between screens:
   
   ```svg
   <!-- Arrow definition in defs section -->
   <defs>
     <marker id="arrowhead" markerWidth="10" markerHeight="7" 
     refX="9" refY="3.5" orient="auto">
       <polygon points="0 0, 10 3.5, 0 7" />
     </marker>
   </defs>
   
   <!-- Arrow usage between screens -->
   <path d="M[start_x],[start_y] Q[control_x],[control_y] [end_x],[end_y]" 
   stroke="#555" stroke-width="2" fill="none" 
   marker-end="url(#arrowhead)" class="arrow" />

2. Arrow Positioning Guidelines:

Start arrows from logical exit points on the source screen (e.g., buttons, links).
End arrows at logical entry points on the target screen (e.g., top or relevant content areas).
Use curved paths (quadratic or cubic Bezier curves) for clean, non-overlapping flows.
Add a small text label near each arrow describing the action (e.g., "Click Submit", "Swipe Left").


3. Multiple Flow Connections:

For screens with multiple outgoing flows, use distinct arrow paths that don't overlap.
Position arrow labels to clearly associate with their respective paths.
Use consistent curve styles for similar types of navigation actions.


4. Visual Characteristics:

Use a stroke width of 2px for arrows in low-fidelity wireframes.
Use a stroke width of 1.5px for arrows in medium and high-fidelity wireframes.
Apply a subtle animation attribute for high-fidelity wireframes (optional).
Add small circles at connection points for better visibility where appropriate.


5. Arrow Types by Interaction:

Primary user flow: Solid line with standard arrow
Optional/alternative flows: Dashed line with standard arrow
Back navigation: Thinner line with smaller arrowhead
System-initiated transitions: Dotted line with standard arrow  


## Implementation Examples to Add

Add these example implementations to help the model understand exactly how to create proper arrows:
Example Screen Flow Arrow:
Here are specific examples showing how to implement different types of arrows for screen flows:
1. Standard flow arrow (e.g., form submission):
```svg<path d="M360,400 Q450,400 520,200" stroke="#555" stroke-width="2" fill="none" marker-end="url(#arrowhead)" class="arrow" />
<text x="430" y="380" class="arrow-label">Submit Form</text>```

2. Optional flow arrow (e.g., skip step):
```svg<path d="M360,450 Q500,500 520,300" stroke="#555" stroke-width="1.5" stroke-dasharray="5,3" fill="none" marker-end="url(#arrowhead)" class="arrow optional" />
<text x="430" y="480" class="arrow-label">Skip</text>```

3. Back navigation arrow:
``` svg<path d="M520,350 Q450,450 360,350" stroke="#777" stroke-width="1.5" fill="none" marker-end="url(#arrowhead)" class="arrow back" />
<text x="430" y="430" class="arrow-label">Back</text> ```

4. Complex user flow with multiple paths:
For screens with multiple possible navigation paths, ensure arrows don't cross by using different curve parameters:
``` svg<!-- Path 1: Approve -->
<path d="M360,300 Q450,250 520,150" stroke="#555" stroke-width="2" fill="none" marker-end="url(#arrowhead)" class="arrow" />
<text x="430" y="250" class="arrow-label">Approve</text>

<!-- Path 2: Reject -->
<path d="M360,350 Q450,450 520,550" stroke="#555" stroke-width="2" fill="none" marker-end="url(#arrowhead)" class="arrow" />
<text x="430" y="450" class="arrow-label">Reject</text>

<!-- Path 3: Request Changes -->
<path d="M360,400 Q300,500 520,650" stroke="#555" stroke-width="2" fill="none" marker-end="url(#arrowhead)" class="arrow" />
<text x="360" y="520" class="arrow-label">Request Changes</text> ```

## CSS Rules to Add to Style Section

Add these CSS rules to the style section of your SVG:

```css
.arrow {{
  stroke-linecap: round;
  stroke-linejoin: round;
}}
.arrow-label {{
  font-size: 12px;
  fill: #555;
  text-anchor: middle;
  font-family: Arial, sans-serif;
}}
.arrow.optional {{
  stroke-dasharray: 5,3;
}}
.arrow.back {{
  stroke: #777;
}} 
```

#### Component Rendering:
- Add subtle visual differentiation between content types.
- Include appropriate placeholder text that indicates content purpose.
- Implement consistent styling for repeated elements across screens.
- Indicate required fields with a visual marker (asterisk or label).

#### Visual Hierarchy:
- Apply appropriate stroke weights based on fidelity level.
- Use a readable, consistent color scheme.
- Ensure sufficient contrast between elements for clarity.
- Implement proper spacing and alignment according to the grid system.

#### Testing and Verification:
- Verify that no text elements overlap with other elements.
- Ensure that icon placeholders contain only ONE type of visual indicator.
- Check that navigation items have clear separation between icon and text.
- Confirm that all interactive elements are clearly distinguishable.

### Output:
 Return the complete SVG code (including all style definitions) that can be directly rendered in a browser.

"""

# the prompt that works very good (Default)
#     prompt = f""" ### Introduction:
# You are an expert SVG wireframe generator specializing in translating wireframe plans into clean, semantic SVG code. Your expertise covers visual design principles, SVG optimization, and creating wireframes at various fidelity levels (low, medium, high).

# ### Context:
# Based on this wireframe plan:
# {plan_json}

# ### Instructions:
# 1. **Analyze the Wireframe Plan:**
#    - Identify all screens/pages that need to be created.
#    - Understand the relationships and flows between screens.
#    - Note the required fidelity level (low, medium, high).
#    - Review any specific style requirements or brand elements.

# 2. **Plan the SVG Structure:**
#    - Determine appropriate viewBox dimensions to accommodate all content (e.g., 360x800 for mobile).
#    - Plan logical positioning of screens with clear separation.
#    - Define a consistent coordinate system (0,0 at top left).
#    - Establish proper spacing between screens (minimum 50px).

# 3. **Design the Styling System:**
#    - Create a comprehensive style section with classes for common elements.
#    - Define appropriate visual characteristics for the specified fidelity level.
#    - Establish color scheme, stroke weights, and fill styles.
#    - Ensure sufficient contrast and visual hierarchy.

# 4. **Implement Each Screen Methodically:**
#    - Start with container and layout elements.
#    - Add primary content blocks following the specified hierarchy.
#    - Implement interactive elements (buttons, forms, menus).
#    - Add text elements with appropriate placeholder content.
#    - Include navigation components as specified.

# 5. **Prevent Element Overlapping:**
#    - Use ONLY ONE visual representation per element (text OR icon OR symbol).
#    - Ensure text labels are positioned separately from visual indicators.
#    - Apply proper spacing between elements (minimum 5px).
#    - Test for potential overlaps visually before finalizing.

# 6. **Review and Optimize:**
#    - Check that all screens match their specifications.
#    - Verify all components are properly positioned and sized.
#    - Ensure consistent styling across similar elements.
#    - Optimize SVG code for cleanliness and efficiency.

# ### Wireframe Requirements:

# #### Fidelity Implementation:
# - **Low-fidelity:** Use basic shapes, simple outlines, minimal text labels, and placeholder blocks.
# - **Medium-fidelity:** Add more defined UI components, basic iconography, text hierarchy, and grid structure.
# - **High-fidelity:** Include detailed components, proper spacing, realistic proportions, and visual hierarchy indicators.

# #### Core Styling Elements:
# 1. **Define a comprehensive style section with classes for:**
#    - `.screen` - Container for each screen (with subtle border).
#    - `.screen-header` - Header section for each screen.
#    - `.screen-title` - Title text for each screen.
#    - `.form-field` - Input field containers.
#    - `.form-label` - Text labels for form fields.
#    - `.button` - Action buttons with appropriate styling for fidelity level.
#    - `.button-label` - Text inside buttons.
#    - `.notification` - Success/error message containers.
#    - `.navbar` - Navigation bar styling.
#    - `.footer` - Footer section styling.
#    - `.content-block` - Generic content containers.
#    - `.arrow` - Connection lines between screens.
#    - `.link-text` - Hyperlinks or navigation text.

# #### Element Representation and Clarity:
# - **For icon placeholders:** Use EITHER a text label OR a simple shape/symbol, NEVER both overlapping.
# - **For navigation items:** Place text labels BELOW or BESIDE icon placeholders with adequate spacing.
# - **For interactive elements:** Use consistent visual indicators that don't interfere with text.
# - **Maintain clear visual separation between different components.**

# #### Technical Specifications:
# - Create responsive SVGs with the `viewBox` attribute set appropriately (e.g., `viewBox="0 0 360 800"` for mobile).
# - Use `width` and `height` attributes set to 100% for responsive scaling.
# - Include proper namespacing and DOCTYPE declarations.
# - Use semantic grouping (`<g>` elements) with descriptive ids for logical sections.

# #### Layout & Organization:
# 1. **Position screens in a logical flow.**
# 2. **Include proper margins between screens (at least 50px).**
# 3. **Use consistent sizing for similar components.**
# 4. **Group related elements together using `<g>` tags with descriptive ids.**
# 5. **Maintain a minimum spacing of 5px between adjacent elements.**

# #### Component Rendering:
# - Add subtle visual differentiation between content types.
# - Include appropriate placeholder text that indicates content purpose.
# - Implement consistent styling for repeated elements across screens.
# - Indicate required fields with a visual marker (asterisk or label).

# #### Visual Hierarchy:
# - Apply appropriate stroke weights based on fidelity level.
# - Use a readable, consistent color scheme.
# - Ensure sufficient contrast between elements for clarity.
# - Implement proper spacing and alignment according to the grid system.

# #### Testing and Verification:
# - Verify that no text elements overlap with other elements.
# - Ensure that icon placeholders contain only ONE type of visual indicator.
# - Check that navigation items have clear separation between icon and text.
# - Confirm that all interactive elements are clearly distinguishable.

# ### Output:
#  Return the complete SVG code (including all style definitions) that can be directly rendered in a browser.

# """
   
    

   
# this propmpt work to some extent but still needs improvements

#     prompt = f""" 
#       ### Introduction:
#       You are an expert SVG wireframe generator specializing in translating wireframe requirements and plans into clean, semantic SVG code. Your expertise covers visual design principles, SVG optimization, and creating wireframes at various fidelity levels (low, medium, high) with a focus on usability, accessibility, and technical implementation.

# ### Context:
# Based on this wireframe requirments and plan:

# #### detailed_requirements: {requirements_json}. 
# #### wireframe_plan: {plan_json}

# ### Instructions:
# 1. **Analyze the Wireframe Plan & User Needs:**
#    - Identify all screens/pages that need to be created
#    - Understand the relationships and flows between screens
#    - Note the required fidelity level (low, medium, high)
#    - Review specific style requirements, brand elements, and user personas
#    - Consider the content strategy and information architecture

# 2. **Plan the SVG Structure & Component System:**
#    - Determine appropriate viewBox dimensions to accommodate all content (e.g., 360x800 for mobile)
#    - Plan logical positioning of screens with clear separation
#    - Define a consistent coordinate system (0,0 at top left)
#    - Establish proper spacing between screens (minimum 50px)
#    - Create a reusable component library approach for common elements

# 3. **Design the Styling System & Accessibility Features:**
#    - Create a comprehensive style section with classes for common elements
#    - Define appropriate visual characteristics for the specified fidelity level
#    - Establish color scheme with proper contrast ratios (minimum 4.5:1 for text)
#    - Define stroke weights, fill styles, and visual states (default, hover, active, disabled)
#    - Include ARIA attributes and focus states for interactive elements

# 4. **Implement Each Screen Methodically:**
#    - Start with container and layout elements following a grid system
#    - Add primary content blocks following the specified information hierarchy
#    - Implement interactive elements (buttons, forms, menus) with proper states
#    - Add text elements with appropriate placeholder content that indicates purpose
#    - Include navigation components with clear visual affordances

# 5. **Prevent Element Overlapping & Enhance Clarity:**
#    - Use ONLY ONE visual representation per element (text OR icon OR symbol)
#    - Ensure text labels are positioned separately from visual indicators
#    - Apply proper spacing between elements (minimum 8px for small elements, 16px for larger sections)
#    - Test for potential overlaps visually before finalizing
#    - Create sufficient white space to improve readability

# 6. **Design for Different States & Interactions:**
#    - Include visual representations for different UI states (empty, loading, error, success)
#    - Create placeholders for micro-interactions and transitions
#    - Design hover and active states for interactive elements
#    - Include feedback mechanisms for user actions
#    - Consider motion design hints where relevant

# 7. **Optimize for Technical Implementation:**
#    - Structure SVG code with developer handoff in mind
#    - Use semantic grouping with descriptive IDs that match development conventions
#    - Include appropriate comments explaining complex sections
#    - Optimize path data and minimize redundant elements
#    - Consider performance implications for complex screens

# 8. **Review, Test & Optimize:**
#    - Check that all screens match their specifications
#    - Verify all components are properly positioned and sized
#    - Ensure consistent styling across similar elements
#    - Test visual hierarchy with squint test (blur vision and check if important elements stand out)
#    - Optimize SVG code for cleanliness and efficiency

# ### Wireframe Requirements:

# #### Fidelity Implementation:
# - **Low-fidelity:** Use basic shapes, simple outlines, minimal text labels, and placeholder blocks. Focus on layout and flow rather than details.
# - **Medium-fidelity:** Add more defined UI components, basic iconography, text hierarchy, and grid structure. Include interactive states and basic visual differentiation.
# - **High-fidelity:** Include detailed components, proper spacing, realistic proportions, and visual hierarchy indicators. Add subtle shadows, gradients, and state variations.

# #### Core Styling Elements:
# 1. **Define a comprehensive style section with classes for:**
#    - `.screen` - Container for each screen (with subtle border)
#    - `.screen-header` - Header section for each screen
#    - `.screen-title` - Title text for each screen
#    - `.form-field` - Input field containers
#    - `.form-label` - Text labels for form fields
#    - `.button` - Action buttons with appropriate styling for fidelity level
#    - `.button-primary` - Primary action buttons with emphasis
#    - `.button-secondary` - Secondary action buttons
#    - `.button-label` - Text inside buttons
#    - `.notification` - Success/error message containers
#    - `.navbar` - Navigation bar styling
#    - `.footer` - Footer section styling
#    - `.content-block` - Generic content containers
#    - `.card` - Container for grouped content
#    - `.arrow` - Connection lines between screens
#    - `.link-text` - Hyperlinks or navigation text
#    - `.icon` - Icon placeholders
#    - `.state-active` - Active state styling
#    - `.state-disabled` - Disabled state styling
#    - `.state-hover` - Hover state styling
#    - `.state-focus` - Focus state styling for accessibility

# #### Element Representation and Clarity:
# - **For icon placeholders:** Use EITHER a text label OR a simple shape/symbol, NEVER both overlapping
# - **For navigation items:** Place text labels BELOW or BESIDE icon placeholders with adequate spacing
# - **For interactive elements:** Use consistent visual indicators that don't interfere with text
# - **Maintain clear visual separation between different components**
# - **Use appropriate visual cues for affordances** (what users can interact with)

# #### Technical Specifications:
# - Create responsive SVGs with the `viewBox` attribute set appropriately (e.g., `viewBox="0 0 360 800"` for mobile)
# - Use `width` and `height` attributes set to 100% for responsive scaling
# - Include proper namespacing and DOCTYPE declarations
# - Use semantic grouping (`<g>` elements) with descriptive ids for logical sections
# - Add `role` and `aria-label` attributes to important interactive elements

# #### Layout & Organization:
# 1. **Position screens in a logical flow that represents the user journey**
# 2. **Include proper margins between screens (at least 50px)**
# 3. **Use consistent sizing for similar components**
# 4. **Group related elements together using `<g>` tags with descriptive ids**
# 5. **Maintain a minimum spacing of 8px between adjacent elements**
# 6. **Follow a consistent grid system** (8px or 4px base grid recommended)

# #### Component Rendering:
# - Add subtle visual differentiation between content types
# - Include appropriate placeholder text that indicates content purpose
# - Implement consistent styling for repeated elements across screens
# - Indicate required fields with a visual marker (asterisk or label)
# - Design empty states for content areas

# #### Visual Hierarchy:
# - Apply appropriate stroke weights based on fidelity level
# - Use a readable, consistent color scheme
# - Ensure sufficient contrast between elements for clarity
# - Implement proper spacing and alignment according to the grid system
# - Size elements according to their importance in the information hierarchy

# #### Testing and Verification:
# - Verify that no text elements overlap with other elements
# - Ensure that icon placeholders contain only ONE type of visual indicator
# - Check that navigation items have clear separation between icon and text
# - Confirm that all interactive elements are clearly distinguishable
# - Test accessibility by ensuring sufficient contrast and clear focus states

# #### Analytics & Measurement Considerations:
# - Include placeholders for tracking elements
# - Mark key conversion points and user journey milestones
# - Consider how design elements support measurement of success metrics

# ### Output:
# Return the complete SVG code (including all style definitions) that can be directly rendered in a browser. Include brief annotations explaining key design decisions and how the wireframe supports the user goals identified in the requirements.

#    """
    
    model = get_llm_model()

    response = model.invoke(prompt)

    try:
        # Extract SVG code from the response
        unstructured_svg_code = extract_svg_from_text(response.content)
        svg_code = clean_svg(unstructured_svg_code)

         # Simple validation
        if not svg_code or ("<svg" not in svg_code and "<!DOCTYPE" not in svg_code):
            raise ValueError("Failed to extract valid SVG code from the model response")
        

        return {
            **state,
            "svg_code": svg_code,
        }
    except Exception as e:
        return {
            **state,
            "errors": (state.get("errors") or []) + [f"Error in SVG generation: {str(e)}"]
        }
    





