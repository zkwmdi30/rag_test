from flask import Flask, request, jsonify
import json
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
import weaviate
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from flask import Flask, request, jsonify
from flask_cors import CORS  # CORS 임포트

app = Flask(__name__)
CORS(app)  # CORS 활성화

# API 엔드포인트: '/query'
@app.route('/query', methods=['GET'])
def query():
    try:
        # 1. 요청에서 질문 받기
        data = request.json
        query = data.get("query")
        if not query:
            return jsonify({"error": "Query is required"}), 400

        # 2. sample.txt 파일 로드
        loader = TextLoader('./sample.txt')
        documents = loader.load()

        # 3. 텍스트 분할
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(documents)

        # 4. Weaviate 클라이언트 설정
        client = weaviate.Client(url="http://localhost:8080")

        # 5. 벡터스토어 생성
        vectorstore = Weaviate.from_documents(
            client=client,    
            documents=chunks,
            embedding=OpenAIEmbeddings(openai_api_key="key"),
            by_text=False
        )

        # 6. 리트리버 설정
        retriever = vectorstore.as_retriever()

        # 7. 프롬프트 템플릿 정의
        template = """You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. 
        Use three sentences maximum and keep the answer concise.
        Question: {question} 
        Context: {context} 
        Answer:
        """
        prompt = ChatPromptTemplate.from_template(template)

        # 8. LLM 모델 설정
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key="key")

        # 9. RAG 체인 정의
        rag_chain = (
            {"context": retriever,  "question": RunnablePassthrough()} 
            | prompt 
            | llm
            | StrOutputParser() 
        )

        # 10. 쿼리 실행
        response = rag_chain.invoke(query)

        # 11. 근거 자료(clues)에서 'text'만 추출하여 JSON으로 직렬화
        clues = retriever.get_relevant_documents(query)
        clues_text = [{"text": doc.page_content, "source": doc.metadata.get("source", "unknown")} for doc in clues]

        # 12. 결과를 JSON 형식으로 변환하고, 근거 자료(clues) 추가
        response_dict = {
            "answer": response,
            "clues": clues_text
        }

        # 13. JSON 응답 반환
        return jsonify(response_dict)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)