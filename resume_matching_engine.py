import math
from collections import defaultdict

─────────────────────────────────────────────
SKILL_ALIASES — exact as given, do not modify
─────────────────────────────────────────────
SKILL_ALIASES = {
    "python": "python", "pyhton": "python",
    "java": "java",
    "javascript": "javascript", "javascrpit": "javascript", "js": "javascript",
    "typescript": "typescript", "typescrpit": "typescript",
    "c++": "cpp", "cpp": "cpp",
    "r": "r",
    "kotlin": "kotlin",
    "machinelearning": "machinelearning", "machine learning": "machinelearning",
    "ml": "machinelearning", "sklearn": "machinelearning",
    "deeplearning": "deeplearning", "deep learning": "deeplearning", "deep-learning": "deep_learning",
    "tensorflow": "tensorflow", "pytorch": "pytorch", "keras": "keras",
    "nlp": "nlp", "bert": "bert", "xgboost": "xgboost",
    "feature engineering": "feature_engineering",
    "statistics": "statistics", "stats": "statistics",
    "regression": "regression", "clustering": "clustering",
    "data-viz": "datavisualization", "data visualization": "datavisualization",
    "data viz": "datavisualization", "matplotlib": "datavisualization",
    "tableau": "datavisualization", "power-bi": "datavisualization",
    "power bi": "datavisualization", "powerbi": "datavisualization",
    "pandas": "pandas", "numpy": "numpy",
    "react": "react", "reacts": "react", "reactjs": "react",
    "vue": "vue", "vue.js": "vue", "vuejs": "vue",
    "redux": "redux", "tailwind": "tailwind",
    "html/css": "htmlcss", "html css": "htmlcss", "html": "htmlcss", "css": "htmlcss",
    "jest": "jest", "graphql": "graphql",
    "node.js": "nodejs", "nodejs": "nodejs", "node js": "nodejs",
    "flask": "flask",
    "spring boot": "springboot", "springboot": "springboot",
    "rest api": "restapi", "rest": "restapi", "restapi": "rest_api",
    "microservices": "microservices",
    "sql": "sql", "mysql": "mysql", "mysq": "mysql",
    "postgresql": "postgresql", "postgres": "postgresql",
    "mongodb": "mongodb", "redis": "redis",
    "docker": "docker",
    "kubernetes": "kubernetes", "kubernates": "kubernetes", "k8s": "kubernetes",
    "ci/cd": "cicd", "cicd": "cicd", "ci cd": "ci_cd",
    "aws": "aws",
    "android": "android", "firebase": "firebase",
    "algorithms": "algorithms", "algoritms": "algorithms",
    "data structure": "datastructures", "data structures": "datastructures",
    "competitive programming": "competitive_programming",
    "ui/ux": "uiux", "ui ux": "uiux", "figma": "figma",
}

Sort by length descending so multi-word phrases match before single tokens
SORTEDKEYS = sorted(SKILLALIASES.keys(), key=lambda x: -len(x))

class ResumeMatcher:
    def init(self):
        self.vocab = set()
        self.vocab_idx = {}
        self.V = 0
        self.N = 0
        self.df = defaultdict(int)
        self.idf = {}
        self.resume_vectors = []
        self.jd_vectors = {}

    def normalize(self, rawskillsstr):
        """Normalize and deduplicate skills"""
        tokens = [t.strip() for t in rawskillsstr.split(",")]
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

    def buildsharedvocabulary(self, resumes):
        """Build shared vocabulary from resumes"""
        for _, skills in resumes:
            self.vocab.update(skills)
        self.vocab = sorted(self.vocab)
        self.vocab_idx = {s: i for i, s in enumerate(self.vocab)}
        self.V = len(self.vocab)
        self.N = len(resumes)

    def computetfidf_vectors(self, resumes):
        """Compute TF-IDF vectors for resumes"""
        for _, skills in resumes:
            for s in skills:
                self.df[s] += 1
        self.idf = {s: math.log(self.N / self.df[s]) for s in self.vocab}
        self.resume_vectors = []
        for name, skills in resumes:
            n = len(skills)
            vec = [0.0] * self.V
            for s in skills:
                tf = 1.0 / n
                vec[self.vocab_idx[s]] = tf * self.idf[s]
            self.resume_vectors.append((name, vec))

    def buildjdbinaryvectors(self, jdraw):
        """Build JD binary vectors"""
        for jdname, raw in jdraw.items():
            jd_skills = self.normalize(raw)
            vec = [0.0] * self.V
            for s in jd_skills:
                if s in self.vocab_idx:
                    vec[self.vocab_idx[s]] = 1.0
            self.jdvectors[jdname] = vec

    def cosine_similarity(self, a, b):
        """Compute cosine similarity between two vectors"""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norma == 0 or normb == 0:
            return 0.0
        return dot / (norma * normb)

    def rank_resumes(self):
        """Rank resumes based on cosine similarity with JDs"""
        print("=" * 50)
        print("  RESUME MATCHING ENGINE — RESULTS")
        print("=" * 50)
        for jdname, jdvec in self.jd_vectors.items():
            scores = []
            for name, rvec in self.resumevectors:
                sim = self.cosinesimilarity(rvec, jd_vec)
                scores.append((name, sim))
            scores.sort(key=lambda x: (-x[1], x[0]))
            top3 = scores[:3]
            print(f"\n{jd_name}")
            print(", ".join(f"{n}({s:.2f})" for n, s in top3))
        print("\n" + "=" * 50)

RAW RESUME DATA (10 candidates)
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

Normalize all resumes
resumes = [(name, ResumeMatcher().normalize(raw)) for name, raw in raw_resumes]

matcher = ResumeMatcher()
matcher.buildsharedvocabulary(resumes)
matcher.computetfidf_vectors(resumes)

JD skills are also normalized through the same alias map
jd_raw = {
    "JD-1 — Kakao (ML Engineer)":
        "Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, SQL, Data Visualization, NLP, BERT, feature engineering, statistics",
    "JD-2 — Naver (Backend Engineer)":
        "Java, Spring Boot, MySQL, PostgreSQL, Microservices, Docker, Kubernetes, REST API, CI/CD, Redis",
    "JD-3 — Line (Frontend Engineer)":
        "JavaScript, React, Vue, TypeScript, REST API, HTML/CSS, Node.js, GraphQL, Redux, Jest, AWS",
}

matcher.buildjdbinaryvectors(jdraw)
matcher.rank_resumes()
