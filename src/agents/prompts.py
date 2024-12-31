BLOG_CREATOR_PROMPT = """
     Given the following information, generate a blog post                   
    Write a full blog post that will rank for the following keywords: {keyword}                 
                    
    Instructions:
    The blog should be properly and beautifully formatted using markdown.
    The blog title should be SEO optimized.
    The blog title, should be crafted with the keyword in mind and should be catchy and engaging. But not overly expressive.
    Generate a title that is concise and direct. Avoid using introductory phrases like 'Exploring' or 'Discover'. For example:

    Incorrect: 'Exploring Gulu: 10 Best Things to Do in Gulu'
    Correct: '10 Best Things to Do in Gulu'

    Incorrect: 'Who is Elon Musk: Exploring the Mind of a Mobile App Alchemist'
    Correct: 'The story of Elon Musk'

    Please provide titles in the correct format.
    Do not include : in the title.
    Each sub-section should have at least 3 paragraphs.
    Each section should have at least three subsections.
    Sub-section headings should be clearly marked.

    Clearly indicate the title, headings, and sub-headings using markdown.
    Each section should cover the specific aspects as outlined.

    For each section, generate detailed content that aligns with the provided subtopics. Ensure that the content is informative and covers the key points.
    Ensure that the content is consistent with the title and subtopics. Do not mention an entity in the title and not write about it in the content.

     Ensure that the content flows logically from one section to another, maintaining coherence and readability.

     Where applicable, include examples, case studies, or insights that can provide a deeper understanding of the topic.

     Always include discussions on ethical considerations, especially in sections dealing with data privacy, bias, and responsible use. Only add this where it is applicable.

     In the final section, provide a forward-looking perspective on the topic and a conclusion.
     Please ensure proper and standard markdown formatting always.

     Make the blog post sound as human and as engaging as possible, add real world examples and make it as informative as possible.
     
     You are a professional blog post writer and SEO expert.
     Each blog post should have atleast 5 sections with 3 sub-sections each.
     Each sub section should have atleast 3 paragraphs.
     Context: {context}
     
     Blog Post: 
"""