import os
import json
import subprocess

import boto3
from dotenv import load_dotenv

load_dotenv(verbose=True)

# リポジトリのURLを変数で指定
repo_url = "https://github.com/totsukash/go-ai-agent-test.git"


def git_clone(repo_url):
    # カレントディレクトリを取得
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # リポジトリ名を取得
    repo_name = os.path.splitext(os.path.basename(repo_url))[0]

    # クローン先のディレクトリパスを作成
    destination_dir = os.path.join(current_dir, "projects", repo_name)

    try:
        # git cloneコマンドを実行
        subprocess.run(["git", "clone", repo_url, destination_dir], check=True)
        print(f"リポジトリ '{repo_name}' のクローンが完了しました。")
    except subprocess.CalledProcessError as e:
        print(f"git cloneの実行中にエラーが発生しました: {e}")


def ai_chat(message) -> str:
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    bedrock_runtime = session.client("bedrock-runtime", region_name="us-east-1")

    prompt_config = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "日本の総理大臣は？"},
                ],
            }
        ],
    }

    body = json.dumps(prompt_config)

    model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    accept = "application/json"
    content_type = "application/json"

    response = bedrock_runtime.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())

    result = response_body.get("content")[0].get("text")
    return result


if __name__ == "__main__":
    # git_clone(repo_url)
    res = ai_chat("こんにちは！")
    print(res)
