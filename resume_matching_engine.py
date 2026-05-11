import math

SKILL_ALIASES = {
    "python": "python", "pyhton": "python",
    "java": "java",
    "javascript": "javascript", "javascrpit": "javascript", "js": "javascript",
    "typescript": "typescript", "typescrpit": "typescript",
    "c++": "cpp", "cpp": "cpp",
    "r": "r",
    "kotlin": "kotlin",
    "machinelearning": "machine_learning", "machine learning": "machine_learning",
    "ml": "machine_learning", "sklearn": "machine_learning",
    "deeplearning": "deep_learning", "deep learning": "deep_learning", "deep-learning": "deep_learning",
    "tensorflow": "tensorflow", "pytorch": "pytorch", "keras": "keras",
    "nlp": "nlp", "bert": "bert", "xgboost": "xgboost",
    "feature engineering": "feature_engineering",
    "statistics": "statistics", "stats": "statistics",
    "regression": "regression", "clustering": "clustering",
    "data-viz": "data_visualization", "data visualization": "data_visualization",
    "data viz": "data_visualization", "matplotlib": "data_visualization",
    "tableau": "data_visualization", "power-bi": "data_visualization",
    "power bi": "data_visualization", "powerbi": "data_visualization",
    "pandas": "pandas", "numpy": "numpy",
    "react": "react", "reacts": "react", "reactjs": "react",
    "vue": "vue", "vue.js": "vue", "vuejs": "vue",
    "redux": "redux", "tailwind": "tailwind",
    "html/css": "html_css", "html css": "html_css", "html": "html_css", "css": "html_css",
    "jest": "jest", "graphql": "graphql",
    "node.js": "nodejs", "nodejs": "nodejs", "node js": "nodejs",
    "flask": "flask",
    "spring boot": "spring_boot", "springboot": "spring_boot",
    "rest api": "rest_api", "rest": "rest_api", "restapi": "rest_api",
    "microservices": "microservices",
    "sql": "sql", "mysql": "mysql", "mysq": "mysql",
    "postgresql": "postgresql", "postgres": "postgresql",
    "mongodb": "mongodb", "redis": "redis",
    "docker": "docker",
    "kubernetes": "kubernetes", "kubernates": "kubernetes", "k8s": "kubernetes",
    "ci/cd": "ci_cd", "cicd": "ci_cd", "ci cd": "ci_cd",
    "aws": "aws",
    "android": "android", "firebase": "firebase",
    "algorithms": "algorithms", "algoritms": "algorithms",
    "data structure": "data_structures", "data structures": "data_structures",
    "competitive programming": "competitive_programming",
    "ui/ux": "ui_ux", "ui ux": "ui_ux", "figma": "figma",
}

SORTED_KEYS = sorted(SKILL_ALIASES.keys(), key=lambda x: -len(x))

def normalize(raw):
    tokens = [t.strip() for t in raw.split(",")]
    canonical = []
    seen = set()
    for token in tokens:
        t = token.lower()
        matched = None
        for key in SORTED_KEYS:
            if t == key:
                matched = SKILL_ALIASES[key]
                break
        if matched and matched not in seen:
            canonical.append(matched)
            seen.add(matched)
    return canonical

raw_resumes = [
    ("Arjun Sharma",    "Pyhton, MachineLearning, SQL, pandas, numpy, Deep-learning"),
    ("Priya Nair",      "JavaScrpit, Reacts, Node.JS, MongoDb, REST api, HTML/CSS"),
    ("Rahul Gupta",     "Java, Spring Boot, MySql, Microservices, Docker, kubernates"),
    ("Sneha Patel",     "Python, TensorFlow, Keras, NLP, BERT, data-viz, matplotlib"),
    ("Vikram Singh",    "C++, Algoritms, Data Structure, competitive programming, python"),
    ("Ananya Krishnan", "javascript, vue.js, python, flask, PostgreSQL, AWS, CI/CD"),
    ("Karan Mehta",     "Python, Sklearn, XGboost, feature engineering, SQL, tableau"),
    ("Deepika Rao",     "Java, Android, Kotlin, Firebase, REST, UI/UX, figma"),
    ("Aditya Kumar",    "Reactjs, TypeScrpit, GraphQL, redux, tailwind, nodejs, jest"),
    ("Meera Iyer",      "python, R, statistics, ML, regression, clustering, Power-BI"),
]

resumes = [(name, normalize(raw)) for name, raw in raw_resumes]

all_skills = set()
for _, skills in resumes:
    all_skills.update(skills)

vocab = sorted(all_skills)
vocab_idx = {s: i for i, s in enumerate(vocab)}
V = len(vocab)
N = len(resumes)

df = {s: 0 for s in vocab}
for _, skills in resumes:
    for s in skills:
        df[s] += 1

idf = {s: math.log(N / df[s]) for s in vocab}

resume_vectors = []
for name, skills in resumes:
    n = len(skills)
    vec = [0.0] * V
    for s in skills:
        tf = 1.0 / n
        vec[vocab_idx[s]] = tf * idf[s]
    resume_vectors.append((name, vec))

jd_raw = {
    "JD-1 -- Kakao (ML Engineer)":
        "Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, SQL, Data Visualization, NLP, BERT, feature engineering, statistics",
    "JD-2 -- Naver (Backend Engineer)":
        "Java, Spring Boot, MySQL, PostgreSQL, Microservices, Docker, Kubernetes, REST API, CI/CD, Redis",
    "JD-3 -- Line (Frontend Engineer)":
        "JavaScript, React, Vue, TypeScript, REST API, HTML/CSS, Node.js, GraphQL, Redux, Jest, AWS",
}

jd_vectors = {}
for jd_name, raw in jd_raw.items():
    jd_skills = normalize(raw)
    vec = [0.0] * V
    for s in jd_skills:
        if s in vocab_idx:
            vec[vocab_idx[s]] = 1.0
    jd_vectors[jd_name] = vec

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

for jd_name, jd_vec in jd_vectors.items():
    scores = []
    for name, r_vec in resume_vectors:
        sim = cosine_similarity(r_vec, jd_vec)
        scores.append((name, sim))
    scores.sort(key=lambda x: (-x[1], x[0]))
    top3 = scores[:3]
    print(jd_name)
    print(", ".join(f"{n}({s:.2f})" for n, s in top3))
    print()
