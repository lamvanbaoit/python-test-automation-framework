#!/usr/bin/env python3
"""
Test Data Validator - Validate test data cho 1000 test cases
"""

import re
import json
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import jsonschema
from jsonschema import validate, ValidationError

@dataclass
class ValidationResult:
    """Kết quả validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    validated_count: int
    invalid_count: int

class TestDataValidator:
    """Validator cho test data"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.schemas = self._load_validation_schemas()
    
    def _load_validation_schemas(self) -> Dict[str, Dict]:
        """Load validation schemas"""
        return {
            "user": {
                "type": "object",
                "required": ["username", "email", "password", "phone"],
                "properties": {
                    "username": {
                        "type": "string",
                        "minLength": 3,
                        "maxLength": 50,
                        "pattern": "^[a-zA-Z0-9_]+$"
                    },
                    "email": {
                        "type": "string",
                        "format": "email",
                        "maxLength": 100
                    },
                    "password": {
                        "type": "string",
                        "minLength": 6,
                        "maxLength": 50
                    },
                    "phone": {
                        "type": "string",
                        "pattern": "^0[0-9]{9}$"
                    },
                    "first_name": {
                        "type": "string",
                        "maxLength": 50
                    },
                    "last_name": {
                        "type": "string",
                        "maxLength": 50
                    },
                    "role": {
                        "type": "string",
                        "enum": ["user", "admin", "moderator"]
                    },
                    "is_active": {
                        "type": "boolean"
                    }
                }
            },
            "product": {
                "type": "object",
                "required": ["name", "price", "category", "sku"],
                "properties": {
                    "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                    },
                    "price": {
                        "type": "number",
                        "minimum": 0
                    },
                    "category": {
                        "type": "string",
                        "enum": ["electronics", "clothing", "books", "food", "sports"]
                    },
                    "sku": {
                        "type": "string",
                        "pattern": "^SKU_[A-Z0-9]{8}$"
                    },
                    "stock": {
                        "type": "integer",
                        "minimum": 0
                    },
                    "description": {
                        "type": "string",
                        "maxLength": 1000
                    }
                }
            },
            "order": {
                "type": "object",
                "required": ["order_id", "user_id", "products", "total_amount"],
                "properties": {
                    "order_id": {
                        "type": "string",
                        "pattern": "^ORD_[A-Z0-9]{8}$"
                    },
                    "user_id": {
                        "type": "string"
                    },
                    "products": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "required": ["product_id", "quantity"],
                            "properties": {
                                "product_id": {
                                    "type": "string"
                                },
                                "quantity": {
                                    "type": "integer",
                                    "minimum": 1
                                },
                                "price": {
                                    "type": "number",
                                    "minimum": 0
                                }
                            }
                        }
                    },
                    "total_amount": {
                        "type": "number",
                        "minimum": 0
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "completed", "cancelled", "failed"]
                    },
                    "created_at": {
                        "type": "string",
                        "format": "date-time"
                    }
                }
            }
        }
    
    def validate_user_data(self, user_data: Dict[str, Any]) -> ValidationResult:
        """Validate user data"""
        return self._validate_data(user_data, "user", "User")
    
    def validate_product_data(self, product_data: Dict[str, Any]) -> ValidationResult:
        """Validate product data"""
        return self._validate_data(product_data, "product", "Product")
    
    def validate_order_data(self, order_data: Dict[str, Any]) -> ValidationResult:
        """Validate order data"""
        return self._validate_data(order_data, "order", "Order")
    
    def validate_test_suite_data(self, suite_data: Dict[str, Any]) -> ValidationResult:
        """Validate test suite data"""
        errors = []
        warnings = []
        validated_count = 0
        invalid_count = 0
        
        # Validate suite structure
        required_fields = ["suite_name", "test_count", "created_at"]
        for field in required_fields:
            if field not in suite_data:
                errors.append(f"Missing required field: {field}")
                invalid_count += 1
            else:
                validated_count += 1
        
        # Validate suite name
        if "suite_name" in suite_data:
            suite_name = suite_data["suite_name"]
            if not isinstance(suite_name, str) or len(suite_name) < 3:
                errors.append("Suite name must be a string with at least 3 characters")
                invalid_count += 1
            elif not re.match(r"^[a-zA-Z0-9_-]+$", suite_name):
                errors.append("Suite name contains invalid characters")
                invalid_count += 1
        
        # Validate test count
        if "test_count" in suite_data:
            test_count = suite_data["test_count"]
            if not isinstance(test_count, int) or test_count <= 0:
                errors.append("Test count must be a positive integer")
                invalid_count += 1
            elif test_count > 10000:
                warnings.append("Test count is very high (>10000)")
        
        # Validate users array
        if "users" in suite_data:
            users = suite_data["users"]
            if not isinstance(users, list):
                errors.append("Users must be an array")
                invalid_count += 1
            else:
                for i, user in enumerate(users):
                    user_result = self.validate_user_data(user)
                    if not user_result.is_valid:
                        errors.extend([f"User {i}: {error}" for error in user_result.errors])
                        invalid_count += 1
                    else:
                        validated_count += 1
                        warnings.extend([f"User {i}: {warning}" for warning in user_result.warnings])
        
        # Validate products array
        if "products" in suite_data:
            products = suite_data["products"]
            if not isinstance(products, list):
                errors.append("Products must be an array")
                invalid_count += 1
            else:
                for i, product in enumerate(products):
                    product_result = self.validate_product_data(product)
                    if not product_result.is_valid:
                        errors.extend([f"Product {i}: {error}" for error in product_result.errors])
                        invalid_count += 1
                    else:
                        validated_count += 1
                        warnings.extend([f"Product {i}: {warning}" for warning in product_result.warnings])
        
        # Validate orders array
        if "orders" in suite_data:
            orders = suite_data["orders"]
            if not isinstance(orders, list):
                errors.append("Orders must be an array")
                invalid_count += 1
            else:
                for i, order in enumerate(orders):
                    order_result = self.validate_order_data(order)
                    if not order_result.is_valid:
                        errors.extend([f"Order {i}: {error}" for error in order_result.errors])
                        invalid_count += 1
                    else:
                        validated_count += 1
                        warnings.extend([f"Order {i}: {warning}" for warning in order_result.warnings])
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            validated_count=validated_count,
            invalid_count=invalid_count
        )
    
    def _validate_data(self, data: Dict[str, Any], schema_type: str, data_type: str) -> ValidationResult:
        """Validate data against schema"""
        errors = []
        warnings = []
        
        try:
            # Validate against JSON schema
            schema = self.schemas.get(schema_type)
            if not schema:
                errors.append(f"Schema not found for {data_type}")
                return ValidationResult(False, errors, warnings, 0, 1)
            
            validate(instance=data, schema=schema)
            
            # Additional custom validations
            custom_errors, custom_warnings = self._custom_validation(data, schema_type)
            errors.extend(custom_errors)
            warnings.extend(custom_warnings)
            
            return ValidationResult(
                is_valid=len(errors) == 0,
                errors=errors,
                warnings=warnings,
                validated_count=1,
                invalid_count=1 if errors else 0
            )
            
        except ValidationError as e:
            errors.append(f"{data_type} validation error: {e.message}")
            return ValidationResult(False, errors, warnings, 0, 1)
        except Exception as e:
            errors.append(f"Unexpected error validating {data_type}: {str(e)}")
            return ValidationResult(False, errors, warnings, 0, 1)
    
    def _custom_validation(self, data: Dict[str, Any], schema_type: str) -> tuple[List[str], List[str]]:
        """Custom validation rules beyond JSON schema"""
        errors = []
        warnings = []
        
        if schema_type == "user":
            # Custom user validation
            if "email" in data:
                email = data["email"]
                if email.endswith("@test.com") and "real" in email.lower():
                    warnings.append("Email contains 'real' but ends with @test.com")
            
            if "phone" in data:
                phone = data["phone"]
                if phone.startswith("000"):
                    warnings.append("Phone number starts with 000")
        
        elif schema_type == "product":
            # Custom product validation
            if "price" in data and "stock" in data:
                price = data["price"]
                stock = data["stock"]
                if price > 1000000 and stock > 100:
                    warnings.append("High price product with high stock")
            
            if "name" in data:
                name = data["name"]
                if len(name) < 5:
                    warnings.append("Product name is very short")
        
        elif schema_type == "order":
            # Custom order validation
            if "products" in data and "total_amount" in data:
                products = data["products"]
                total_amount = data["total_amount"]
                
                calculated_total = sum(
                    p.get("price", 0) * p.get("quantity", 1) 
                    for p in products
                )
                
                if abs(calculated_total - total_amount) > 0.01:
                    errors.append(f"Total amount mismatch: calculated {calculated_total}, provided {total_amount}")
            
            if "created_at" in data:
                try:
                    datetime.fromisoformat(data["created_at"].replace('Z', '+00:00'))
                except ValueError:
                    errors.append("Invalid date format in created_at")
        
        return errors, warnings
    
    def validate_file(self, file_path: str, data_type: str) -> ValidationResult:
        """Validate data from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if data_type == "user":
                return self.validate_user_data(data)
            elif data_type == "product":
                return self.validate_product_data(data)
            elif data_type == "order":
                return self.validate_order_data(data)
            elif data_type == "suite":
                return self.validate_test_suite_data(data)
            else:
                return ValidationResult(False, [f"Unknown data type: {data_type}"], [], 0, 1)
                
        except FileNotFoundError:
            return ValidationResult(False, [f"File not found: {file_path}"], [], 0, 1)
        except json.JSONDecodeError as e:
            return ValidationResult(False, [f"Invalid JSON in file: {e}"], [], 0, 1)
        except Exception as e:
            return ValidationResult(False, [f"Error reading file: {e}"], [], 0, 1)
    
    def validate_directory(self, directory_path: str, data_type: str) -> ValidationResult:
        """Validate all files in directory"""
        import os
        
        errors = []
        warnings = []
        validated_count = 0
        invalid_count = 0
        
        try:
            for filename in os.listdir(directory_path):
                if filename.endswith('.json'):
                    file_path = os.path.join(directory_path, filename)
                    result = self.validate_file(file_path, data_type)
                    
                    if result.is_valid:
                        validated_count += result.validated_count
                        warnings.extend([f"{filename}: {w}" for w in result.warnings])
                    else:
                        invalid_count += result.invalid_count
                        errors.extend([f"{filename}: {e}" for e in result.errors])
                        warnings.extend([f"{filename}: {w}" for w in result.warnings])
            
            return ValidationResult(
                is_valid=len(errors) == 0,
                errors=errors,
                warnings=warnings,
                validated_count=validated_count,
                invalid_count=invalid_count
            )
            
        except Exception as e:
            return ValidationResult(False, [f"Error reading directory: {e}"], [], 0, 1)
    
    def generate_validation_report(self, results: List[ValidationResult]) -> Dict[str, Any]:
        """Generate validation report"""
        total_validated = sum(r.validated_count for r in results)
        total_invalid = sum(r.invalid_count for r in results)
        total_errors = sum(len(r.errors) for r in results)
        total_warnings = sum(len(r.warnings) for r in results)
        
        return {
            "summary": {
                "total_validated": total_validated,
                "total_invalid": total_invalid,
                "total_errors": total_errors,
                "total_warnings": total_warnings,
                "success_rate": total_validated / (total_validated + total_invalid) * 100 if (total_validated + total_invalid) > 0 else 0
            },
            "details": [
                {
                    "index": i,
                    "is_valid": r.is_valid,
                    "errors": r.errors,
                    "warnings": r.warnings,
                    "validated_count": r.validated_count,
                    "invalid_count": r.invalid_count
                }
                for i, r in enumerate(results)
            ],
            "timestamp": datetime.now().isoformat()
        }

# Global validator instance
test_data_validator = TestDataValidator() 