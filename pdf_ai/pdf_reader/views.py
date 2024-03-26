from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import UploadedPDF
from .forms import UploadMultiplePDFForm


def upload_pdf(request):
    form = UploadMultiplePDFForm(request.POST, request.FILES)

    if request.method == 'POST':
        pdf_files = request.FILES.getlist('pdf_files')
        valid_files = []
        invalid_files = []

        for file in pdf_files:
            if not file.content_type.startswith('application/pdf'):
                invalid_files.append(file.name)
            else:
                valid_files.append(file)

        if invalid_files:
            error_message = f"Invalid file types detected: {', '.join(invalid_files)} (Only PDF files are allowed)"
            context = {'form': form, 'error_message': error_message}
            return render(request, "download_pdf.html", context)

        files = []
        for file in valid_files:
            pdf_file = UploadedPDF(pdf_files = file)
            pdf_file.save()
            files.append(pdf_file.pdf_files.path)

        # save all file's pathes in session json variable to use it in ai_assistent() view
        request.session['files'] = files

        return redirect('ai_assistent')
    
    context = {'form': form}

    return render(request, "download_pdf.html", context)

def ai_assistent(request):
    if request.method == 'GET':

        return render(request, "ai_assistent.html", {})
    
    elif request.method == 'POST':

        # get all file's pathes from session json variable
        files = request.session['files']
        # create list of PyPDFLoader objects with file's path parameters
        loaders = [PyPDFLoader(file) for file in files]

        docs = []
        for loader in loaders:
            docs.extend(loader.load())

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1500,
            chunk_overlap = 150
        )

        # make splits of all pdf documents (Also be better implement splitting by sections and get section's name in answer)
        splits = text_splitter.split_documents(docs)

        embedding = OpenAIEmbeddings()

        persist_directory = 'docs/chroma/'

        vectordb = Chroma.from_documents(
            documents=splits,
            embedding=embedding,
            persist_directory=persist_directory
        )

        llm = ChatOpenAI(temperature=0)

        # create prompt message to llm
        template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer. 
        {context}
        Question: {question}
        """
        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
        qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=vectordb.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )

        # get question from textarea
        question = request.POST.get('question')

        result = qa_chain.invoke({"query": question})

        # The problem is it always splits pdf files and creates Chroma database each POST request, so it slows the program

        return JsonResponse({'answer': result['result']})
