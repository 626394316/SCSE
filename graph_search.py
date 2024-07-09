def get_knowledge_graph(question, llm, graph):
    graph_schema = """
    Node properties are the following:
    subject {use: STRING, purpose: STRING, examRequirement: STRING, definition: STRING, name: STRING, learn: STRING},book {publish: STRING, time: STRING, autor: STRING, bookName: STRING},knowledge {content: STRING, name: STRING, disadvantage: STRING, advantage: STRING},organization {name: STRING, description: STRING},periodical {name: STRING, time: STRING}
    Relationship properties are the following:

    The relationships are the following:
    (:subject)-[:会议]->(:periodical),(:subject)-[:预备知识]->(:subject),(:subject)-[:相关教材]->(:book),(:subject)-[:基本概念]->(:knowledge),(:subject)-[:基本方法]->(:knowledge),(:subject)-[:工业应用]->(:knowledge),(:subject)-[:商业应用]->(:knowledge),(:subject)-[:医学应用]->(:knowledge),(:subject)-[:安全应用]->(:knowledge),(:subject)-[:军事应用]->(:knowledge),(:subject)-[:办公应用]->(:knowledge),(:subject)-[:研究组织]->(:organization),(:subject)-[:期刊]->(:periodical),(:organization)-[:包含]->(:organization)
    """

    cypher_generation = f"""
    Task:Generate Cypher statement to query a graph database.
    Instructions:
    Use only the provided relationship types and properties in the schema.
    Do not use any other relationship types or properties that are not provided.
    Schema:
    {graph_schema}

    Note: Do not include any explanations or apologies in your responses.
    Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
    Do not include any text except the generated Cypher statement.

    The question is:
    {question}
    """

    result1 = llm.predict(cypher_generation)

    try:
        result2 = graph.query(result1)
    except Exception as e:
        result2 = []

    if result2 == []:
        result3 = []
    else:
        qa = f"""
        You are an assistant that helps to form nice and human understandable answers.
        The information part contains the provided information that you must use to construct an answer.
        The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
        Make the answer sound as a response to the question. Do not mention that you based the result on the given information.
        Here is an example:
        Question: Which managers own Neo4j stocks?
        Context:[manager:CTL LLC, manager:JANE STREET GROUP LLC]
        Helpful Answer: CTL LLC, JANE STREET GROUP LLC owns Neo4j stocks.
        Follow this example when generating answers.
        If the provided information is empty, say that you don't know the answer.
        Information:
        {result2}
        Question: {question}
        Helpful Answer:
        """

        result3 = llm.predict(qa)
    return result3
