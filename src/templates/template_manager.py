"""
Template manager for SimuServer - handles loading and managing API templates
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

class TemplateManager:
    """Manages API templates for different services"""
    
    def __init__(self, templates_dir: Optional[str] = None):
        if templates_dir:
            self.templates_dir = Path(templates_dir)
        else:
            self.templates_dir = Path(__file__).parent / "presets"
        
        # Ensure templates directory exists
        self.templates_dir.mkdir(exist_ok=True)
        
        # Create default templates if they don't exist
        self._create_default_templates()
    
    def _create_default_templates(self):
        """Create default API templates"""
        
        # Instagram-like API template
        instagram_template = {
            "name": "Instagram API",
            "description": "Simulates Instagram-like social media API endpoints",
            "version": "1.0",
            "routes": [
                {
                    "method": "GET",
                    "path": "/api/instagram/users/me",
                    "response": {
                        "id": 12345,
                        "username": "john_doe",
                        "full_name": "John Doe",
                        "profile_picture": "https://example.com/profile.jpg",
                        "bio": "Just another Instagram user",
                        "followers_count": 150,
                        "following_count": 200,
                        "posts_count": 42
                    }
                },
                {
                    "method": "GET",
                    "path": "/api/instagram/posts",
                    "response": {
                        "data": [
                            {
                                "id": "post_001",
                                "user": {
                                    "id": 12345,
                                    "username": "john_doe"
                                },
                                "caption": "Beautiful sunset today! 🌅",
                                "image_url": "https://example.com/sunset.jpg",
                                "likes_count": 42,
                                "comments_count": 5,
                                "created_time": "2025-07-15T18:30:00Z"
                            }
                        ],
                        "pagination": {
                            "next_url": "/api/instagram/posts?max_id=post_000"
                        }
                    }
                },
                {
                    "method": "POST",
                    "path": "/api/instagram/posts",
                    "response": {
                        "id": "post_new",
                        "status": "posted",
                        "message": "Post created successfully"
                    }
                },
                {
                    "method": "POST",
                    "path": "/api/instagram/posts/{post_id}/like",
                    "response": {
                        "status": "liked",
                        "likes_count": 43
                    }
                }
            ]
        }
        
        # Messenger-like API template
        messenger_template = {
            "name": "Messenger API",
            "description": "Simulates messaging app API endpoints",
            "version": "1.0",
            "routes": [
                {
                    "method": "GET",
                    "path": "/api/messenger/conversations",
                    "response": {
                        "conversations": [
                            {
                                "id": "conv_001",
                                "participants": [
                                    {"id": 1, "name": "John Doe"},
                                    {"id": 2, "name": "Jane Smith"}
                                ],
                                "last_message": {
                                    "id": "msg_100",
                                    "text": "Hey, how are you?",
                                    "sender_id": 2,
                                    "timestamp": "2025-07-15T10:30:00Z"
                                },
                                "unread_count": 2
                            }
                        ]
                    }
                },
                {
                    "method": "GET",
                    "path": "/api/messenger/conversations/{conversation_id}/messages",
                    "response": {
                        "messages": [
                            {
                                "id": "msg_099",
                                "text": "Hi there!",
                                "sender_id": 1,
                                "timestamp": "2025-07-15T10:25:00Z"
                            },
                            {
                                "id": "msg_100",
                                "text": "Hey, how are you?",
                                "sender_id": 2,
                                "timestamp": "2025-07-15T10:30:00Z"
                            }
                        ]
                    }
                },
                {
                    "method": "POST",
                    "path": "/api/messenger/conversations/{conversation_id}/messages",
                    "response": {
                        "id": "msg_new",
                        "status": "sent",
                        "timestamp": "2025-07-15T10:35:00Z"
                    }
                }
            ]
        }
        
        # Twitter-like API template
        twitter_template = {
            "name": "Twitter API",
            "description": "Simulates Twitter-like microblogging API endpoints",
            "version": "1.0",
            "routes": [
                {
                    "method": "GET",
                    "path": "/api/twitter/timeline",
                    "response": {
                        "tweets": [
                            {
                                "id": "tweet_001",
                                "text": "Just deployed a new feature! 🚀",
                                "user": {
                                    "id": 1,
                                    "username": "developer_joe",
                                    "display_name": "Joe Developer"
                                },
                                "created_at": "2025-07-15T12:00:00Z",
                                "retweet_count": 5,
                                "like_count": 23,
                                "reply_count": 2
                            }
                        ]
                    }
                },
                {
                    "method": "POST",
                    "path": "/api/twitter/tweets",
                    "response": {
                        "id": "tweet_new",
                        "status": "published",
                        "created_at": "2025-07-15T12:05:00Z"
                    }
                },
                {
                    "method": "POST",
                    "path": "/api/twitter/tweets/{tweet_id}/like",
                    "response": {
                        "status": "liked",
                        "like_count": 24
                    }
                }
            ]
        }
        
        # E-commerce API template
        ecommerce_template = {
            "name": "E-commerce API",
            "description": "Simulates online store API endpoints",
            "version": "1.0",
            "routes": [
                {
                    "method": "GET",
                    "path": "/api/ecommerce/products",
                    "response": {
                        "products": [
                            {
                                "id": 1,
                                "name": "Awesome T-Shirt",
                                "description": "A really awesome t-shirt",
                                "price": 29.99,
                                "currency": "USD",
                                "category": "clothing",
                                "in_stock": True,
                                "stock_quantity": 50,
                                "images": [
                                    "https://example.com/tshirt1.jpg"
                                ]
                            }
                        ],
                        "pagination": {
                            "page": 1,
                            "per_page": 20,
                            "total": 150
                        }
                    }
                },
                {
                    "method": "GET",
                    "path": "/api/ecommerce/cart",
                    "response": {
                        "items": [
                            {
                                "product_id": 1,
                                "quantity": 2,
                                "price": 29.99
                            }
                        ],
                        "total": 59.98,
                        "currency": "USD"
                    }
                },
                {
                    "method": "POST",
                    "path": "/api/ecommerce/cart/add",
                    "response": {
                        "status": "added",
                        "cart_total": 89.97
                    }
                },
                {
                    "method": "POST",
                    "path": "/api/ecommerce/checkout",
                    "response": {
                        "order_id": "order_12345",
                        "status": "processing",
                        "total": 89.97,
                        "estimated_delivery": "2025-07-20"
                    }
                }
            ]
        }
        
        # Authentication API template
        auth_template = {
            "name": "Authentication API",
            "description": "Simulates user authentication and authorization endpoints",
            "version": "1.0",
            "routes": [
                {
                    "method": "POST",
                    "path": "/api/auth/login",
                    "response": {
                        "status": "success",
                        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refresh_token": "refresh_token_123",
                        "expires_in": 3600,
                        "user": {
                            "id": 1,
                            "email": "user@example.com",
                            "name": "John Doe"
                        }
                    }
                },
                {
                    "method": "POST",
                    "path": "/api/auth/register",
                    "response": {
                        "status": "success",
                        "message": "User registered successfully",
                        "user_id": 123
                    }
                },
                {
                    "method": "POST",
                    "path": "/api/auth/refresh",
                    "response": {
                        "token": "new_jwt_token_here",
                        "expires_in": 3600
                    }
                },
                {
                    "method": "POST",
                    "path": "/api/auth/logout",
                    "response": {
                        "status": "success",
                        "message": "Logged out successfully"
                    }
                }
            ]
        }
        
        # Save templates
        templates = {
            "instagram.json": instagram_template,
            "messenger.json": messenger_template,
            "twitter.json": twitter_template,
            "ecommerce.json": ecommerce_template,
            "auth.json": auth_template
        }
        
        for filename, template_data in templates.items():
            template_path = self.templates_dir / filename
            if not template_path.exists():
                with open(template_path, 'w') as f:
                    json.dump(template_data, f, indent=2)
    
    def get_available_templates(self) -> List[Tuple[str, str]]:
        """Get list of available templates (name, description)"""
        templates = []
        
        for template_file in self.templates_dir.glob("*.json"):
            try:
                with open(template_file, 'r') as f:
                    template_data = json.load(f)
                    name = template_data.get("name", template_file.stem)
                    description = template_data.get("description", "No description")
                    templates.append((name, description))
            except Exception as e:
                print(f"Error loading template {template_file}: {e}")
        
        return templates
    
    def get_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Get template data by name"""
        # Try to find template by name
        for template_file in self.templates_dir.glob("*.json"):
            try:
                with open(template_file, 'r') as f:
                    template_data = json.load(f)
                    if template_data.get("name") == template_name:
                        return template_data
            except Exception as e:
                print(f"Error loading template {template_file}: {e}")
        
        return None
    
    def save_template(self, template_name: str, template_data: Dict[str, Any]) -> bool:
        """Save a template to file"""
        try:
            # Sanitize filename
            filename = template_name.lower().replace(" ", "_").replace("-", "_")
            filename = "".join(c for c in filename if c.isalnum() or c == "_")
            template_path = self.templates_dir / f"{filename}.json"
            
            with open(template_path, 'w') as f:
                json.dump(template_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving template: {e}")
            return False
    
    def delete_template(self, template_name: str) -> bool:
        """Delete a template"""
        for template_file in self.templates_dir.glob("*.json"):
            try:
                with open(template_file, 'r') as f:
                    template_data = json.load(f)
                    if template_data.get("name") == template_name:
                        template_file.unlink()
                        return True
            except Exception as e:
                print(f"Error deleting template {template_file}: {e}")
        
        return False 