# 飞书文档完美写入工作流
# 使用官方 API，确保 block 顺序正确

import requests
import json
import uuid
from typing import List, Dict, Any, Optional

class FeishuDocPerfectWriter:
    """
    飞书文档完美写入器
    使用官方 API，确保内容顺序完全正确
    """
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.base_url = "https://open.feishu.cn/open-apis"
        
    def _get_access_token(self) -> str:
        """获取访问令牌"""
        url = f"{self.base_url}/auth/v3/app_access_token/internal"
        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        if result.get("code") == 0:
            self.access_token = result["tenant_access_token"]
            return self.access_token
        else:
            raise Exception(f"获取 token 失败: {result}")
    
    def _ensure_token(self):
        """确保 token 有效"""
        if not self.access_token:
            self._get_access_token()
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """发送 API 请求"""
        self._ensure_token()
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))
        
        response = requests.request(method, url, headers=headers, **kwargs)
        result = response.json()
        
        # Token 过期，重新获取
        if result.get("code") == 99991663:
            self.access_token = None
            self._ensure_token()
            headers["Authorization"] = f"Bearer {self.access_token}"
            response = requests.request(method, url, headers=headers, **kwargs)
            result = response.json()
        
        return result
    
    def create_document(self, title: str, folder_token: Optional[str] = None) -> str:
        """
        创建新文档
        
        Args:
            title: 文档标题
            folder_token: 文件夹 token（可选）
        
        Returns:
            document_id: 文档 ID
        """
        endpoint = "/docx/v1/documents"
        data = {
            "title": title
        }
        if folder_token:
            data["folder_token"] = folder_token
        
        result = self._request("POST", endpoint, json=data)
        
        if result.get("code") == 0:
            return result["data"]["document"]["document_id"]
        else:
            raise Exception(f"创建文档失败: {result}")
    
    def get_document_info(self, document_id: str) -> Dict:
        """获取文档信息"""
        endpoint = f"/docx/v1/documents/{document_id}"
        result = self._request("GET", endpoint)
        return result
    
    def get_blocks(self, document_id: str, page_token: Optional[str] = None) -> List[Dict]:
        """
        获取文档 block 列表
        
        注意：返回的 blocks 是按文档顺序排列的
        """
        endpoint = f"/docx/v1/documents/{document_id}/blocks"
        params = {}
        if page_token:
            params["page_token"] = page_token
        
        result = self._request("GET", endpoint, params=params)
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取 blocks 失败: {result}")
    
    def append_blocks(self, document_id: str, block_id: str, 
                      blocks: List[Dict], index: int = -1) -> Dict:
        """
        在指定位置插入 blocks
        
        Args:
            document_id: 文档 ID
            block_id: 父 block ID（文档根节点通常是文档 ID）
            blocks: 要插入的 blocks 列表
            index: 插入位置，-1 表示末尾
        
        Returns:
            插入结果
        """
        endpoint = f"/docx/v1/documents/{document_id}/blocks/{block_id}/children"
        data = {
            "children": blocks
        }
        if index >= 0:
            data["index"] = index
        
        result = self._request("POST", endpoint, json=data)
        return result
    
    def update_block(self, document_id: str, block_id: str, 
                     content: Dict) -> Dict:
        """更新 block 内容"""
        endpoint = f"/docx/v1/documents/{document_id}/blocks/{block_id}"
        data = {
            "update_body": content
        }
        result = self._request("PATCH", endpoint, json=data)
        return result
    
    def delete_block(self, document_id: str, block_id: str) -> Dict:
        """删除 block"""
        endpoint = f"/docx/v1/documents/{document_id}/blocks/{block_id}"
        result = self._request("DELETE", endpoint)
        return result


class FeishuDocContentBuilder:
    """
    飞书文档内容构建器
    用于构建各种 block 类型的内容
    """
    
    @staticmethod
    def create_heading(text: str, level: int = 1) -> Dict:
        """创建标题 block"""
        block_type_map = {1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 8}
        block_type = block_type_map.get(level, 3)
        return {
            "block_type": block_type,
            f"heading{level}": {
                "elements": [
                    {
                        "text_run": {
                            "content": text
                        }
                    }
                ]
            }
        }
    
    @staticmethod
    def create_paragraph(text: str, bold: bool = False, 
                        italic: bool = False) -> Dict:
        """创建段落 block"""
        style = {}
        if bold:
            style["bold"] = True
        if italic:
            style["italic"] = True
        
        element = {
            "text_run": {
                "content": text
            }
        }
        if style:
            element["text_run"]["text_element_style"] = style
        
        return {
            "block_type": 2,
            "text": {
                "elements": [element]
            }
        }
    
    @staticmethod
    def create_bullet_list(text: str) -> Dict:
        """创建无序列表 block"""
        return {
            "block_type": 12,
            "bullet": {
                "elements": [
                    {
                        "text_run": {
                            "content": text
                        }
                    }
                ]
            }
        }
    
    @staticmethod
    def create_ordered_list(text: str, number: int = 1) -> Dict:
        """创建有序列表 block"""
        return {
            "block_type": 13,
            "ordered": {
                "elements": [
                    {
                        "text_run": {
                            "content": text
                        }
                    }
                ],
                "style": {
                    "sequence": str(number)
                }
            }
        }
    
    @staticmethod
    def create_code_block(code: str, language: str = "plain") -> Dict:
        """创建代码块"""
        return {
            "block_type": 14,
            "code": {
                "elements": [
                    {
                        "text_run": {
                            "content": code
                        }
                    }
                ],
                "style": {
                    "language": language
                }
            }
        }
    
    @staticmethod
    def create_divider() -> Dict:
        """创建分隔线"""
        return {
            "block_type": 22,
            "divider": {}
        }
    
    @staticmethod
    def create_table(rows: int, cols: int, 
                     cells: List[List[str]]) -> Dict:
        """创建表格 - 使用正确的 children 格式
        
        注意：由于 Feishu API 限制，表格需要在创建后单独填充内容。
        这个方法返回表格结构，但内容需要通过 PerfectDocumentWriter.create_document_with_content
        或手动调用 fill_table_cells 来填充。
        """
        table_cells = []
        cell_contents = []
        
        for row_idx in range(rows):
            for col_idx in range(cols):
                cell_content = cells[row_idx][col_idx] if row_idx < len(cells) and col_idx < len(cells[row_idx]) else ""
                # 创建空的 table_cell
                table_cells.append({
                    "block_type": 32,
                    "table_cell": {
                        "children": []
                    }
                })
                # 保存内容用于后续填充
                cell_contents.append(cell_content)
        
        return {
            "block_type": 31,
            "table": {
                "row_size": rows,
                "column_size": cols,
                "children": table_cells,
                "property": {
                    "row_size": rows,
                    "column_size": cols
                }
            },
            "_cell_contents": cell_contents  # 内部使用，存储 cell 内容
        }


class PerfectDocumentWriter:
    """
    完美文档写入器
    封装所有操作，确保顺序正确
    """
    
    def __init__(self, app_id: str, app_secret: str):
        self.writer = FeishuDocPerfectWriter(app_id, app_secret)
        self.builder = FeishuDocContentBuilder()
    
    def create_document_with_content(self, title: str, 
                                     content_blocks: List[Dict],
                                     folder_token: Optional[str] = None) -> str:
        """
        创建文档并写入内容（保证顺序）
        
        Args:
            title: 文档标题
            content_blocks: 内容 blocks 列表（按顺序）
            folder_token: 文件夹 token
        
        Returns:
            document_id: 文档 ID
        """
        # 1. 创建文档
        doc_id = self.writer.create_document(title, folder_token)
        
        # 2. 获取文档根 block ID
        doc_info = self.writer.get_document_info(doc_id)
        root_block_id = doc_info["data"]["document"]["document_id"]
        
        # 3. 处理 blocks，提取表格内容
        processed_blocks = []
        table_data = []  # 存储表格的 cell 内容
        
        for block in content_blocks:
            if block.get("block_type") == 31 and "_cell_contents" in block:
                # 这是表格，需要特殊处理
                cell_contents = block.pop("_cell_contents")
                table_data.append({
                    "block_index": len(processed_blocks),
                    "cell_contents": cell_contents
                })
            processed_blocks.append(block)
        
        # 4. 按顺序逐个插入 blocks
        batch_size = 50
        for i in range(0, len(processed_blocks), batch_size):
            batch = processed_blocks[i:i + batch_size]
            result = self.writer.append_blocks(doc_id, root_block_id, batch)
            
            if result.get("code") != 0:
                raise Exception(f"插入 blocks 失败: {result}")
        
        # 5. 填充表格内容
        if table_data:
            # 获取刚创建的 blocks
            try:
                items = self.writer.get_blocks(doc_id)
                
                # 按顺序找到所有表格 blocks
                table_items = []
                for item in items:
                    if item["block_type"] == 31:
                        table_items.append(item)
                
                # 按顺序匹配表格和数据
                for i, table_info in enumerate(table_data):
                    if i < len(table_items):
                        table_block = table_items[i]
                        cell_ids = table_block.get("children", [])
                        cell_contents = table_info["cell_contents"]
                        
                        print(f"填充表格 {i+1}: {len(cell_ids)} cells, {len(cell_contents)} contents")
                        
                        # 向每个 cell 追加内容
                        for cell_idx, cell_id in enumerate(cell_ids):
                            if cell_idx < len(cell_contents):
                                content = cell_contents[cell_idx]
                                text_block = {
                                    "block_type": 2,
                                    "text": {
                                        "elements": [
                                            {
                                                "text_run": {
                                                    "content": content,
                                                    "text_element_style": {}
                                                }
                                            }
                                        ]
                                    }
                                }
                                result = self.writer.append_blocks(doc_id, cell_id, [text_block])
                                if result.get("code") != 0:
                                    print(f"警告: 填充表格 cell {cell_idx} 失败: {result}")
                                else:
                                    print(f"  ✓ Cell {cell_idx}: {content[:20]}...")
            except Exception as e:
                print(f"警告: 填充表格内容时出错: {e}")
        
        return doc_id
    
    def append_content_to_document(self, document_id: str, 
                                   content_blocks: List[Dict]) -> None:
        """
        向现有文档追加内容（保证顺序）
        """
        # 获取文档根 block ID
        doc_info = self.writer.get_document_info(document_id)
        root_block_id = doc_info["data"]["document"]["document_id"]
        
        # 处理 blocks，提取表格内容
        processed_blocks = []
        table_data = []
        
        for block in content_blocks:
            if block.get("block_type") == 31 and "_cell_contents" in block:
                cell_contents = block.pop("_cell_contents")
                table_data.append({
                    "block_index": len(processed_blocks),
                    "cell_contents": cell_contents
                })
            processed_blocks.append(block)
        
        # 按顺序逐个插入
        batch_size = 50
        for i in range(0, len(processed_blocks), batch_size):
            batch = processed_blocks[i:i + batch_size]
            result = self.writer.append_blocks(document_id, root_block_id, batch)
            
            if result.get("code") != 0:
                raise Exception(f"追加 blocks 失败: {result}")
        
        # 填充表格内容
        if table_data:
            try:
                items = self.writer.get_blocks(document_id)
                
                # 按顺序找到所有表格 blocks
                table_items = []
                for item in items:
                    if item["block_type"] == 31:
                        table_items.append(item)
                
                # 按顺序匹配表格和数据
                for i, table_info in enumerate(table_data):
                    if i < len(table_items):
                        table_block = table_items[i]
                        cell_ids = table_block.get("children", [])
                        cell_contents = table_info["cell_contents"]
                        
                        for cell_idx, cell_id in enumerate(cell_ids):
                            if cell_idx < len(cell_contents):
                                content = cell_contents[cell_idx]
                                text_block = {
                                    "block_type": 2,
                                    "text": {
                                        "elements": [
                                            {
                                                "text_run": {
                                                    "content": content,
                                                    "text_element_style": {}
                                                }
                                            }
                                        ]
                                    }
                                }
                                result = self.writer.append_blocks(document_id, cell_id, [text_block])
                                if result.get("code") != 0:
                                    print(f"警告: 填充表格 cell {cell_idx} 失败: {result}")
            except Exception as e:
                print(f"警告: 填充表格内容时出错: {e}")


# ============ 使用示例 ============

if __name__ == "__main__":
    # 初始化
    APP_ID = "cli_xxxxxxxxxx"
    APP_SECRET = "xxxxxxxxxx"
    
    writer = PerfectDocumentWriter(APP_ID, APP_SECRET)
    builder = FeishuDocContentBuilder()
    
    # 构建内容（按顺序）
    content = []
    
    # 1. 标题
    content.append(builder.create_heading("抖音热点监测日报", 1))
    
    # 2. 日期信息
    content.append(builder.create_paragraph("**报告日期：** 2026年2月24日"))
    content.append(builder.create_paragraph("**数据来源：** 抖音热榜"))
    content.append(builder.create_divider())
    
    # 3. 第一部分
    content.append(builder.create_heading("一、全网 TOP10 热点", 2))
    content.append(builder.create_bullet_list("德国总理默茨将访华 - 1209万热度"))
    content.append(builder.create_bullet_list("又到一年返程时 - 1183万热度"))
    content.append(builder.create_bullet_list("复工飒气穿搭拿捏了 - 1020万热度"))
    
    # 4. 第二部分
    content.append(builder.create_heading("二、消费领域热点", 2))
    content.append(builder.create_paragraph("复工穿搭是今日最大消费热点..."))
    
    # 5. 分隔线
    content.append(builder.create_divider())
    
    # 6. 结尾
    content.append(builder.create_paragraph("*报告生成时间：2026-02-24 07:00*", italic=True))
    
    # 创建文档（保证顺序）
    doc_id = writer.create_document_with_content(
        title="抖音热点监测日报 - 20260224",
        content_blocks=content
    )
    
    print(f"文档创建成功: {doc_id}")
    print(f"文档链接: https://feishu.cn/docx/{doc_id}")
