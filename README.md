# Leave Manager - FastAPI

Converted from the supplied Node.js/Express backend.

Architecture:
Router -> Middleware/Dependency -> Service -> Model/Repository -> PostgreSQL

Important behavior:
- Signup does NOT return or create a token.
- Signin creates the JWT and places it in the `token` HTTP-only cookie.
- Existing endpoint names are retained.
- Original obvious bugs are corrected where they prevent intended behavior:
  signup actually inserts the user, `pending` is stored consistently, `purpose` is stored correctly, and response status/message is returned correctly.
- SQL is parameterized.
- Cloudinary secrets are environment variables.
- Original response message text is retained where possible, including existing spelling such as `Submited`, `Conflig`, `Fteched`, and `Libary` to avoid unnecessary frontend changes.

Run:
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload --port 2000

Swagger:
http://localhost:2000/docs
