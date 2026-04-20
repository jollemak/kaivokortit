Project Plan: Well Card SaaS
This document outlines the step-by-step development process for a multi-tenant SaaS application designed to extract "well cards" (kaivokortit) from PDF files using Mistral OCR and Azure Blob Storage.

Phase 1: Infrastructure and Configuration
[ ] Azure Blob Storage: Create a Storage Account and a container named "well-cards".

[ ] Lifecycle Management: Configure a policy to automatically delete files after 7 days.

[ ] Environment Variables: Update config.py to include AZURE_STORAGE_CONNECTION_STRING.

[ ] Database: Set up a PostgreSQL database.

Phase 2: Data Models (SQLAlchemy)
[ ] Create models.py and define the following:

Document: id, company_id (Microsoft Tenant ID), file_hash (SHA-256), and azure_blob_name.

WellCard: id, document_id, page_number, and metadata_json (to store Mistral OCR results).

[ ] Create database.py for session management.

Phase 3: Azure Storage Service
[ ] Create services/storage.py:

Implement a function to upload files to Azure.

Implement a function to generate dynamic, short-lived (e.g., 15 min) SAS URLs.

Phase 4: AI Logic Update
[ ] Update services/ai.py:

Modify analyze_pdf to accept and process a document_url (the SAS URL).

Ensure the OCR output contains necessary coordinates or text for identification.

Phase 5: Backend Core Logic (FastAPI)
[ ] Update main.py:

File Identification: Calculate the SHA-256 hash of the uploaded file.

Cache Check: If the file_hash + company_id exists in the database, return the cached metadata.

Analysis Flow: If the file is new: upload to Azure -> generate SAS URL -> request Mistral OCR analysis -> save results to the database.

Phase 6: Well Card Extraction
[ ] Create a new endpoint POST /ocr/extract:

Allow users to send a list of selected pages or card IDs.

Retrieve the original file from Azure using a new SAS URL.

Use the PyMuPDF (fitz) library to extract only the requested pages.

Return the newly generated PDF to the user.

Phase 7: Authentication and Admin Roles
[ ] Integrate Microsoft Entra ID (OAuth2) for user authentication.

[ ] Implement middleware or a dependency to distinguish between Admin and standard users.

[ ] Ensure all database queries are strictly filtered by company_id for multi-tenant security.