# DS_Team_Project
Hello we are one of the best DS developers Team at GoIT DS_9 flow. 

"AI Docs Researcher" allows users to easily access advanced technologies for processing and analyzing text information 
using modern methods of artificial intelligence.

The main functionality of the project includes:

1. Your files multi-format support:
- Ability to upload documents in PDF, CSV, DOCX, EML, EPUB, HTML, MD, PPTX, TXT formats.
- Ability to attach any weblink that does not require authorization

2. Text processing and analysis of your documents using the powerful capabilities of Large Language Models (LLM):
- used FAISS for vectorization and saving data in a vectorized database
- used OpenAI for embeddings
- used OpenAI like LLM

3. How to use it:
- Interact with processed documents via chat to get contextually informed answers.
- if the data from the current document is not enough to provide a reasoned answer to the question, 
   then you can always add additional documents and expand the current context with new data
- this way you can always choose how to work: only with data from one or several documents at once
- options for working with chats offer: creating a new chat, viewing chat history, merging chats, deleting chats
- When you delete a chat, all its data and associated documents are deleted forever

4. User privacy:
- Email verification functionality that allows you to confirm that the specified email address belongs to the user.
- Using JWT (JSON Web Tokens) for user authentication and authorization. JWT ensures the security of data transfer 
between client and server by using a signed token.
- The ability to reset the user's password by email.
- Ability to create and edit user profiles, save users data in the database.
- all users can work only with their documents.
- data, files and history of requests to LLM available only for the user

5. Admin abilities:
- Separation of users by roles such as admin, moderator and regular user. Each role will have appropriate access 
rights to the functionality of the web service.
- Redis is used to limit the number of requests and cache data to improve performance

6. "AI Docs Researcher" uses technologies such as: FastAPI, Streamlit, PostgreSQL, Docker, OpenAI, Faiss, Git, LangChain, Cloudinary, Redis.


# How to start for developers:
- unload project from Git

- create in root folder your own .env file like .env.example

- run docker application

- run in terminal: `docker-compose up` -> up application for use

### Shut off

- terminal with docker run: `docker-compose down` -> shut off application


# Good luck!!!