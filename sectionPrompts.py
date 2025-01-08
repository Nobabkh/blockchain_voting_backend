





# UPDATED_USER_PROMT = """
# for any prompt your response should be inside html tag not text on markdown should be there if your name is asked then you should say genAI inside html tag and h1 tag always wrap text in html tag.
# """

# UPDATED_USER_PROMT_2 = """
# You are GenWebBuilder. You are created by ExciteAI Limited. You can generate website from images, sketch design, and crawler. When anyone want to know about yourself you should answer from this content, otherwise say I dont know or This question is not relevent wrape your answer in html tag. avoid using markdown or plain text. You generate website from, 
# """


def assemble_prompt_for_section(generated_code_config: str, codelist: list[str], userprompt: str):
    # Set the system prompt based on the output settings
    
    user_content = [
        {
            "type": "text",
            "text": "please update the code of "+codelist[2]+"and follow "+userprompt,
        },
    ]

    system_content = [
        {
            "type": "text",
            "text": (
                "You are an expert " + generated_code_config + " developer. "
                "You need to modify the code given by user"
                "Please provide the output in plain JSON format with no markdown or code formatting. "
                "The JSON structure should be: "
                '{"code": "place body here", "style": "place additional styles here", "script": "place additional scripts here"}. '
                "Do not add any extra formatting or text. Just output the JSON."
            ),
        },
    ]


    return [
        {
            "role": "system",
            "content": system_content,
        },
        {
            "role": "user",
            "content": user_content,
        },
    ]
