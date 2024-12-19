from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from .models import Profile, Profile_Detail, Career, Skill, Certificate, Language

# 초안
# 각 항목을 구별하여 따로 저장하는 시스템 으로 변경 구상중

def create_profile_document(profile_detail):
    """Profile_Detail 정보만을 문서화하는 함수"""
    content = f"""
    기술스택:
    {', '.join([skill.name for skill in profile_detail.skills.all()])}
    
    경력사항:
    {' '.join([f'{career.company_name}에서 {career.position}으로 근무 ({career.description})' for career in profile_detail.careers.all()])}
    
    학력:
    {' '.join([f'{edu.school_name} {edu.major} ({edu.status})'for edu in profile_detail.educations.all()])}
    
    자격증:
    {', '.join([f'{cert.name} ({cert.issuing_org})' 
                for cert in profile_detail.certificates.all()])}
    
    교육이수:
    {', '.join([f'{edu.education_name}: {edu.description}' 
                for edu in profile_detail.education_contents.all()])}
    
    언어능력:
    {', '.join([lang.description for lang in profile_detail.languages.all()])}
    자기소개: 
    {profile_detail.introduction}
    """
    
    return {"content": content, "metadata": {"profile_id": profile.profile_id}}

def build_vector_store():
    """FAISS 벡터 저장소 구축"""
    # 임베딩 모델 설정
    embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
    
    # Profile_Detail 데이터 가져오기 (관련 데이터 미리 로드)
    profile_details = Profile_Detail.objects.all().prefetch_related(
        'skills',
        'careers',
        'educations',
        'certificates',
        'education_contents',
        'languages'
    ).select_related('profile')
    
    # 프로필 문서 생성
    documents = []
    for profile_detail in profile_details:
        doc = create_profile_document(profile_detail)
        documents.append(doc)
    
    # FAISS 벡터 저장소 생성
    vector_store = FAISS.from_texts(
        texts=[doc["content"] for doc in documents],
        embedding=embeddings,
        metadatas=[doc["metadata"] for doc in documents]
    )
    
    # 저장소 저장
    vector_store.save_local("profile_vector_store")
    return vector_store

def search_similar_profiles(query: str, k: int = 5):
    """유사한 프로필 검색"""
    vector_store = load_vector_store()
    results = vector_store.similarity_search_with_score(query, k=k)
    
    similar_profiles = []
    for doc, score in results:
        profile_id = doc.metadata['profile_id']
        try:
            profile_detail = Profile_Detail.objects.select_related('profile').get(
                profile__profile_id=profile_id
            )
            similar_profiles.append({
                'profile_detail': profile_detail,
                'score': score
            })
        except Profile_Detail.DoesNotExist:
            continue
    
    return similar_profiles