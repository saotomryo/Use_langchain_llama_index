from dotenv import load_dotenv
load_dotenv()

from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
import secret_keys  # 外部ファイルにAPI keyを保存

import os
os.environ["OPENAI_API_KEY"] = secret_keys.openai_api_key

# インデックスの作成
documents = SimpleDirectoryReader("Data").load_data()
faq_index = GPTVectorStoreIndex.from_documents(documents)

# インデックスの保存
faq_index.storage_context.persist("index")
