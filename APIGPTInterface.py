        openai.organization = "org-sJKmIJcaBArbQj7rgC64jN7g"
        # A REMPLACER 
        # openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = "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"
        # openai.Model.list() liste des modeles de openai

        response = openai.Completion.create(
          engine="text-davinci-002",
          prompt="Translate the following English text to French: '{}'",
          max_tokens=60
        )

        print(response.choices[0].text.strip())