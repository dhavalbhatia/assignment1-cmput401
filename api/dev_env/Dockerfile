FROM python:3.10 AS builder

WORKDIR /api
RUN pip install pipenv

# Tell pipenv to create venv in the current directory
ENV PIPENV_VENV_IN_PROJECT=1
ADD Pipfile.lock Pipfile /api/
RUN pipenv install --system
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Use below for prod image 

# FROM python:3.10 AS runtime

# WORKDIR /api
# # copy venv to runtime stage
# RUN mkdir -v /api/.venv
# COPY --from=builder /api/.venv/ /api/.venv/
# ENV PATH="/api/.venv/bin:$PATH"


# RUN adduser --uid 420 pet_app
# USER pet_app
# COPY pet_app /api

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]