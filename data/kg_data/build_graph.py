import json
from neo4j import GraphDatabase
import yaml

#
with open("../../config.yml", 'r', encoding='utf-8') as f:
  configs = yaml.load(f.read(), Loader=yaml.FullLoader)

class Neo4jHandler:
    def __init__(self, url, user, password,database):
        self.driver = GraphDatabase.driver(url, auth=(user, password),database=database)

    def close(self):
        self.driver.close()

    def import_data(self, nodes, relationships):
        with self.driver.session() as session:
            # 导入节点
            for node in nodes:
                print(node)
                session.execute_write(self.create_node, node['n'])
            # 导入关系
            for relationship in relationships:
                for segment in relationship['p']['segments']:
                    session.execute_write(self.create_relationship, segment)

    @staticmethod
    def create_node(tx, node_data):
        print(node_data)
        labels = node_data['labels']
        properties = node_data['properties']
        element_id=node_data["elementId"]
        properties["elementId"]=element_id
        labels_str = ':'.join(labels)
        query = f"CREATE (n:{labels_str} {{"
        query += ', '.join([f"{key}: ${key}" for key in properties.keys()])
        query += "})"
        tx.run(query, **properties)

    @staticmethod
    def create_relationship(tx, segment):
        start_identity = segment['start']["elementId"]
        end_identity = segment['end']["elementId"]
        start_labels=segment["start"]["labels"][0]
        end_labels=segment["end"]["labels"][0]
        relationship_type = segment['relationship']['type']
        query = f"""
        MATCH (a:{start_labels} {{elementId:"{start_identity}"}}), (b:{end_labels} {{elementId:"{end_identity}"}})
        CREATE (a)-[r:{relationship_type}]->(b)
        RETURN r
        """
        tx.run(query, start_id=start_identity, end_id=end_identity)

    def export_data(self):
        with self.driver.session() as session:
            nodes = session.run("MATCH (n) RETURN n,labels(n) as labels").data()
            relationships = session.run("MATCH p=()-->() RETURN p ").data()

            return nodes, relationships


# 使用示例
if __name__ == "__main__":

    # Neo4j 数据库连接信息
    url = configs['neo4j_url']
    user = configs['neo4j_username']
    password = configs['neo4j_password']
    database = configs['neo4j_database']

    with open('pr_node.json', 'r', encoding='utf-8-sig') as file:
      nodes_data = json.load(file)

    with open('pr_rel.json', 'r', encoding='utf-8-sig') as file:
      relationships_data = json.load(file)


#     # 节点和关系数据
#     nodes_data = [
#   {
#     "n": {
#       "identity": 43,
#       "labels": [
#         "subject"
#       ],
#       "properties": {
#         "learn": "",
#         "purpose": "用机器完成类似于人类智能通过视觉、听觉等感官去识别外界环境所进行的工作",
#         "use": "语音识别、图像识别等",
#         "examRequirement": "平时成绩（到课、作业、实验报告）30%期末考试 70%",
#         "name": "模式识别",
#         "definition": "研究用数学方法使计算机自动识别事物的一门科学",
#         "__csv_id": "0"
#       },
#       "elementId": "43"
#     }
#   },
#   {
#     "n": {
#       "identity": 44,
#       "labels": [
#         "subject"
#       ],
#       "properties": {
#         "learn": "向量、矩阵的基本运算、逆、行列式、特征值、特征向量等",
#         "purpose": "",
#         "use": "",
#         "examRequirement": "",
#         "name": "线性代数",
#         "definition": "",
#         "__csv_id": "1"
#       },
#       "elementId": "44"
#     }
#   },
#   {
#     "n": {
#       "identity": 45,
#       "labels": [
#         "subject"
#       ],
#       "properties": {
#         "learn": "概率（先验、条件）、概率密度、随机变量和分布、数学期望、全概率和贝叶斯公式、正态分布、参数估计、假设检验",
#         "purpose": "",
#         "use": "",
#         "examRequirement": "",
#         "name": "概率论与数理统计",
#         "definition": "",
#         "__csv_id": "2"
#       },
#       "elementId": "45"
#     }
#   },
#   {
#     "n": {
#       "identity": 46,
#       "labels": [
#         "subject"
#       ],
#       "properties": {
#         "learn": "null",
#         "purpose": "",
#         "use": "",
#         "examRequirement": "",
#         "name": "高等数学",
#         "definition": "",
#         "__csv_id": "3"
#       },
#       "elementId": "46"
#     }
#   },
#   {
#     "n": {
#       "identity": 47,
#       "labels": [
#         "subject"
#       ],
#       "properties": {
#         "learn": "null",
#         "purpose": "",
#         "use": "",
#         "examRequirement": "",
#         "name": "最优化方法",
#         "definition": "",
#         "__csv_id": "4"
#       },
#       "elementId": "47"
#     }
#   },
#   {
#     "n": {
#       "identity": 48,
#       "labels": [
#         "subject"
#       ],
#       "properties": {
#         "learn": "null",
#         "purpose": "",
#         "use": "",
#         "examRequirement": "",
#         "name": "信息论",
#         "definition": "",
#         "__csv_id": "5"
#       },
#       "elementId": "48"
#     }
#   },
#   {
#     "n": {
#       "identity": 49,
#       "labels": [
#         "subject"
#       ],
#       "properties": {
#         "learn": "null",
#         "purpose": "",
#         "use": "",
#         "examRequirement": "",
#         "name": "程序设计基础",
#         "definition": "",
#         "__csv_id": "6"
#       },
#       "elementId": "49"
#     }
#   }
# ]
#
#     relationships_data = [
#   {
#     "p": {
#       "start": {
#         "identity": 43,
#         "labels": [
#           "subject"
#         ],
#         "properties": {
#           "learn": "",
#           "purpose": "用机器完成类似于人类智能通过视觉、听觉等感官去识别外界环境所进行的工作",
#           "use": "语音识别、图像识别等",
#           "examRequirement": "平时成绩（到课、作业、实验报告）30%期末考试 70%",
#           "name": "模式识别",
#           "definition": "研究用数学方法使计算机自动识别事物的一门科学",
#           "__csv_id": "0"
#         },
#         "elementId": "43"
#       },
#       "end": {
#         "identity": 45,
#         "labels": [
#           "subject"
#         ],
#         "properties": {
#           "learn": "概率（先验、条件）、概率密度、随机变量和分布、数学期望、全概率和贝叶斯公式、正态分布、参数估计、假设检验",
#           "purpose": "",
#           "use": "",
#           "examRequirement": "",
#           "name": "概率论与数理统计",
#           "definition": "",
#           "__csv_id": "2"
#         },
#         "elementId": "45"
#       },
#       "segments": [
#         {
#           "start": {
#             "identity": 43,
#             "labels": [
#               "subject"
#             ],
#             "properties": {
#               "learn": "",
#               "purpose": "用机器完成类似于人类智能通过视觉、听觉等感官去识别外界环境所进行的工作",
#               "use": "语音识别、图像识别等",
#               "examRequirement": "平时成绩（到课、作业、实验报告）30%期末考试 70%",
#               "name": "模式识别",
#               "definition": "研究用数学方法使计算机自动识别事物的一门科学",
#               "__csv_id": "0"
#             },
#             "elementId": "43"
#           },
#           "relationship": {
#             "identity": 1,
#             "start": 43,
#             "end": 45,
#             "type": "预备知识",
#             "properties": {
#
#             },
#             "elementId": "1",
#             "startNodeElementId": "43",
#             "endNodeElementId": "45"
#           },
#           "end": {
#             "identity": 45,
#             "labels": [
#               "subject"
#             ],
#             "properties": {
#               "learn": "概率（先验、条件）、概率密度、随机变量和分布、数学期望、全概率和贝叶斯公式、正态分布、参数估计、假设检验",
#               "purpose": "",
#               "use": "",
#               "examRequirement": "",
#               "name": "概率论与数理统计",
#               "definition": "",
#               "__csv_id": "2"
#             },
#             "elementId": "45"
#           }
#         }
#       ],
#       "length": 1.0
#     }
#   },
#   {
#     "p": {
#       "start": {
#         "identity": 43,
#         "labels": [
#           "subject"
#         ],
#         "properties": {
#           "learn": "",
#           "purpose": "用机器完成类似于人类智能通过视觉、听觉等感官去识别外界环境所进行的工作",
#           "use": "语音识别、图像识别等",
#           "examRequirement": "平时成绩（到课、作业、实验报告）30%期末考试 70%",
#           "name": "模式识别",
#           "definition": "研究用数学方法使计算机自动识别事物的一门科学",
#           "__csv_id": "0"
#         },
#         "elementId": "43"
#       },
#       "end": {
#         "identity": 46,
#         "labels": [
#           "subject"
#         ],
#         "properties": {
#           "learn": "null",
#           "purpose": "",
#           "use": "",
#           "examRequirement": "",
#           "name": "高等数学",
#           "definition": "",
#           "__csv_id": "3"
#         },
#         "elementId": "46"
#       },
#       "segments": [
#         {
#           "start": {
#             "identity": 43,
#             "labels": [
#               "subject"
#             ],
#             "properties": {
#               "learn": "",
#               "purpose": "用机器完成类似于人类智能通过视觉、听觉等感官去识别外界环境所进行的工作",
#               "use": "语音识别、图像识别等",
#               "examRequirement": "平时成绩（到课、作业、实验报告）30%期末考试 70%",
#               "name": "模式识别",
#               "definition": "研究用数学方法使计算机自动识别事物的一门科学",
#               "__csv_id": "0"
#             },
#             "elementId": "43"
#           },
#           "relationship": {
#             "identity": 2,
#             "start": 43,
#             "end": 46,
#             "type": "预备知识",
#             "properties": {
#
#             },
#             "elementId": "2",
#             "startNodeElementId": "43",
#             "endNodeElementId": "46"
#           },
#           "end": {
#             "identity": 46,
#             "labels": [
#               "subject"
#             ],
#             "properties": {
#               "learn": "null",
#               "purpose": "",
#               "use": "",
#               "examRequirement": "",
#               "name": "高等数学",
#               "definition": "",
#               "__csv_id": "3"
#             },
#             "elementId": "46"
#           }
#         }
#       ],
#       "length": 1.0
#     }
#   },
#   {
#     "p": {
#       "start": {
#         "identity": 43,
#         "labels": [
#           "subject"
#         ],
#         "properties": {
#           "learn": "",
#           "purpose": "用机器完成类似于人类智能通过视觉、听觉等感官去识别外界环境所进行的工作",
#           "use": "语音识别、图像识别等",
#           "examRequirement": "平时成绩（到课、作业、实验报告）30%期末考试 70%",
#           "name": "模式识别",
#           "definition": "研究用数学方法使计算机自动识别事物的一门科学",
#           "__csv_id": "0"
#         },
#         "elementId": "43"
#       },
#       "end": {
#         "identity": 47,
#         "labels": [
#           "subject"
#         ],
#         "properties": {
#           "learn": "null",
#           "purpose": "",
#           "use": "",
#           "examRequirement": "",
#           "name": "最优化方法",
#           "definition": "",
#           "__csv_id": "4"
#         },
#         "elementId": "47"
#       },
#       "segments": [
#         {
#           "start": {
#             "identity": 43,
#             "labels": [
#               "subject"
#             ],
#             "properties": {
#               "learn": "",
#               "purpose": "用机器完成类似于人类智能通过视觉、听觉等感官去识别外界环境所进行的工作",
#               "use": "语音识别、图像识别等",
#               "examRequirement": "平时成绩（到课、作业、实验报告）30%期末考试 70%",
#               "name": "模式识别",
#               "definition": "研究用数学方法使计算机自动识别事物的一门科学",
#               "__csv_id": "0"
#             },
#             "elementId": "43"
#           },
#           "relationship": {
#             "identity": 3,
#             "start": 43,
#             "end": 47,
#             "type": "预备知识",
#             "properties": {
#
#             },
#             "elementId": "3",
#             "startNodeElementId": "43",
#             "endNodeElementId": "47"
#           },
#           "end": {
#             "identity": 47,
#             "labels": [
#               "subject"
#             ],
#             "properties": {
#               "learn": "null",
#               "purpose": "",
#               "use": "",
#               "examRequirement": "",
#               "name": "最优化方法",
#               "definition": "",
#               "__csv_id": "4"
#             },
#             "elementId": "47"
#           }
#         }
#       ],
#       "length": 1.0
#     }
#   },
#   {
#     "p": {
#       "start": {
#         "identity": 43,
#         "labels": [
#           "subject"
#         ],
#         "properties": {
#           "learn": "",
#           "purpose": "用机器完成类似于人类智能通过视觉、听觉等感官去识别外界环境所进行的工作",
#           "use": "语音识别、图像识别等",
#           "examRequirement": "平时成绩（到课、作业、实验报告）30%期末考试 70%",
#           "name": "模式识别",
#           "definition": "研究用数学方法使计算机自动识别事物的一门科学",
#           "__csv_id": "0"
#         },
#         "elementId": "43"
#       },
#       "end": {
#         "identity": 48,
#         "labels": [
#           "subject"
#         ],
#         "properties": {
#           "learn": "null",
#           "purpose": "",
#           "use": "",
#           "examRequirement": "",
#           "name": "信息论",
#           "definition": "",
#           "__csv_id": "5"
#         },
#         "elementId": "48"
#       },
#       "segments": [
#         {
#           "start": {
#             "identity": 43,
#             "labels": [
#               "subject"
#             ],
#             "properties": {
#               "learn": "",
#               "purpose": "用机器完成类似于人类智能通过视觉、听觉等感官去识别外界环境所进行的工作",
#               "use": "语音识别、图像识别等",
#               "examRequirement": "平时成绩（到课、作业、实验报告）30%期末考试 70%",
#               "name": "模式识别",
#               "definition": "研究用数学方法使计算机自动识别事物的一门科学",
#               "__csv_id": "0"
#             },
#             "elementId": "43"
#           },
#           "relationship": {
#             "identity": 4,
#             "start": 43,
#             "end": 48,
#             "type": "预备知识",
#             "properties": {
#
#             },
#             "elementId": "4",
#             "startNodeElementId": "43",
#             "endNodeElementId": "48"
#           },
#           "end": {
#             "identity": 48,
#             "labels": [
#               "subject"
#             ],
#             "properties": {
#               "learn": "null",
#               "purpose": "",
#               "use": "",
#               "examRequirement": "",
#               "name": "信息论",
#               "definition": "",
#               "__csv_id": "5"
#             },
#             "elementId": "48"
#           }
#         }
#       ],
#       "length": 1.0
#     }
#   },
#   {
#     "p": {
#       "start": {
#         "identity": 43,
#         "labels": [
#           "subject"
#         ],
#         "properties": {
#           "learn": "",
#           "purpose": "用机器完成类似于人类智能通过视觉、听觉等感官去识别外界环境所进行的工作",
#           "use": "语音识别、图像识别等",
#           "examRequirement": "平时成绩（到课、作业、实验报告）30%期末考试 70%",
#           "name": "模式识别",
#           "definition": "研究用数学方法使计算机自动识别事物的一门科学",
#           "__csv_id": "0"
#         },
#         "elementId": "43"
#       },
#       "end": {
#         "identity": 49,
#         "labels": [
#           "subject"
#         ],
#         "properties": {
#           "learn": "null",
#           "purpose": "",
#           "use": "",
#           "examRequirement": "",
#           "name": "程序设计基础",
#           "definition": "",
#           "__csv_id": "6"
#         },
#         "elementId": "49"
#       },
#       "segments": [
#         {
#           "start": {
#             "identity": 43,
#             "labels": [
#               "subject"
#             ],
#             "properties": {
#               "learn": "",
#               "purpose": "用机器完成类似于人类智能通过视觉、听觉等感官去识别外界环境所进行的工作",
#               "use": "语音识别、图像识别等",
#               "examRequirement": "平时成绩（到课、作业、实验报告）30%期末考试 70%",
#               "name": "模式识别",
#               "definition": "研究用数学方法使计算机自动识别事物的一门科学",
#               "__csv_id": "0"
#             },
#             "elementId": "43"
#           },
#           "relationship": {
#             "identity": 5,
#             "start": 43,
#             "end": 49,
#             "type": "预备知识",
#             "properties": {
#
#             },
#             "elementId": "5",
#             "startNodeElementId": "43",
#             "endNodeElementId": "49"
#           },
#           "end": {
#             "identity": 49,
#             "labels": [
#               "subject"
#             ],
#             "properties": {
#               "learn": "null",
#               "purpose": "",
#               "use": "",
#               "examRequirement": "",
#               "name": "程序设计基础",
#               "definition": "",
#               "__csv_id": "6"
#             },
#             "elementId": "49"
#           }
#         }
#       ],
#       "length": 1.0
#     }
#   }
# ]

    # 创建 Neo4jHandler 实例并导入数据

    neo4j_handler = Neo4jHandler(url, user, password,database)

    neo4j_handler.import_data(nodes_data, relationships_data)

