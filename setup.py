"""
LangGraph Agent 服务安装脚本
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README文件
README_PATH = Path(__file__).parent / "README.md"
if README_PATH.exists():
    with open(README_PATH, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "基于 LangGraph 构建的智能 Agent 服务，集成 Google Gemini 模型"

# 读取requirements文件
REQUIREMENTS_PATH = Path(__file__).parent / "requirements.txt"
if REQUIREMENTS_PATH.exists():
    with open(REQUIREMENTS_PATH, "r", encoding="utf-8") as f:
        install_requires = [
            line.strip() for line in f.readlines()
            if line.strip() and not line.startswith("#")
        ]
else:
    install_requires = []

setup(
    name="langgraph-agent",
    version="1.0.0",
    author="LangGraph Agent Team",
    author_email="contact@langgraph-agent.com",
    description="基于 LangGraph 构建的智能 Agent 服务，集成 Google Gemini 模型",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/langgraph-agent",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.20.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "pre-commit>=2.17.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.20.0",
            "pytest-cov>=4.0.0",
            "httpx>=0.24.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "langgraph-agent=langgraph_agent.main:run_server",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="langgraph, agent, ai, chatbot, gemini, fastapi",
    project_urls={
        "Bug Reports": "https://github.com/your-username/langgraph-agent/issues",
        "Source": "https://github.com/your-username/langgraph-agent",
        "Documentation": "https://github.com/your-username/langgraph-agent#readme",
    },
) 