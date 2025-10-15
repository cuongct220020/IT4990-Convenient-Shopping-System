# 🐍 Python OOP Conventions

## 🎯 Goals
- Write readable, maintainable code
- Ensure consistency across the project
- Support effective team collaboration

**Remember**: Code for humans to read, not just for machines to execute. Consistency > Cleverness.

---

## 📋 Table of Contents
1. [Naming Conventions](#naming-conventions)
2. [Standard Class Structure](#standard-class-structure)
3. [General Principles](#general-principles)
4. [Visibility (Public/Protected/Private)](#visibility)
5. [Comments & Docstrings](#comments--docstrings)
6. [Magic Methods](#magic-methods)
7. [Constants & Configuration](#constants--configuration)
8. [Code Organization](#code-organization)
9. [Inheritance & Composition](#inheritance--composition)
10. [Advanced Best Practices](#advanced-best-practices)
11. [SOLID Principles](#solid-principles)
12. [Review Checklist](#review-checklist)

---

## 1. Naming Conventions

| Component | Convention | Example |
|-----------|-----------|---------|
| Class | PascalCase | `ShoppingList`, `FoodItem` |
| Method | snake_case | `add_to_cart()` |
| Instance Attribute | snake_case | `expiry_date` |
| Class Attribute | snake_case | `max_storage_days` |
| Private Attribute/Method | `_prefix` | `_check_expiry()` |
| Name Mangling | `__prefix` | `__user_token` |
| Constant | UPPER_CASE | `MAX_ITEMS = 100` |
| Module (file) | snake_case | `food_storage.py` |
| Package (folder) | snake_case | `shopping_management/` |

**Rules**:
- Class names are nouns: `FoodItem`, `ShoppingList`
- Method names are verbs: `add_item()`, `check_expiry()`
- Avoid vague names: `MyClass`, `Manager`
- Avoid unclear abbreviations: `fd` → `food`

---

## 2. Standard Class Structure

```python
from datetime import datetime, timedelta
from typing import List, Optional

class FoodItem:
    """
    Represents a food item in the refrigerator.
    
    Attributes:
        EXPIRY_WARNING_DAYS (int): Days to warn before expiration
        name (str): Food name
        quantity (float): Quantity
        unit (str): Unit (kg, gram, liter, etc.)
        expiry_date (datetime): Expiration date
        category (str): Category (vegetables, meat, dry goods, etc.)
    """

    # ✅ 1. Class attributes
    EXPIRY_WARNING_DAYS = 3
    _total_items = 0

    # ✅ 2. Constructor
    def __init__(
        self, 
        name: str, 
        quantity: float, 
        unit: str,
        expiry_date: datetime,
        category: str = "Other"
    ):
        """Initialize food item."""
        self.name = name
        self._quantity = quantity
        self.unit = unit
        self.expiry_date = expiry_date
        self.category = category
        self.__purchase_date = datetime.now()
        FoodItem._total_items += 1

    # ✅ 3. Magic/Dunder methods
    def __str__(self) -> str:
        """User-friendly string representation."""
        return f"{self.name} ({self._quantity}{self.unit}) - Exp: {self.expiry_date.strftime('%m/%d/%Y')}"

    def __repr__(self) -> str:
        """Debug string representation."""
        return f"FoodItem(name='{self.name}', quantity={self._quantity}, unit='{self.unit}')"

    def __eq__(self, other) -> bool:
        """Compare two food items by name and category."""
        if not isinstance(other, FoodItem):
            return NotImplemented
        return self.name == other.name and self.category == other.category

    def __lt__(self, other) -> bool:
        """Compare for sorting by expiration date."""
        if not isinstance(other, FoodItem):
            return NotImplemented
        return self.expiry_date < other.expiry_date

    # ✅ 4. Properties (Pythonic getter/setter)
    @property
    def quantity(self) -> float:
        """Return food quantity."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: float):
        """Update quantity with validation."""
        if value < 0:
            raise ValueError("Quantity cannot be negative.")
        self._quantity = value

    @property
    def days_until_expiry(self) -> int:
        """Calculate days until expiration."""
        delta = self.expiry_date - datetime.now()
        return delta.days

    @property
    def is_expiring_soon(self) -> bool:
        """Check if food is expiring soon."""
        return 0 <= self.days_until_expiry <= self.EXPIRY_WARNING_DAYS

    @property
    def is_expired(self) -> bool:
        """Check if food is expired."""
        return self.days_until_expiry < 0

    # ✅ 5. Public instance methods
    def use(self, amount: float):
        """
        Use a certain amount of food.
        
        Args:
            amount: Amount to use
            
        Raises:
            ValueError: If insufficient quantity
        """
        if amount > self._quantity:
            raise ValueError(f"Not enough {self.name}. Remaining: {self._quantity}{self.unit}")
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        self._quantity -= amount

    def add_quantity(self, amount: float):
        """Add food quantity."""
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        self._quantity += amount

    # ✅ 6. Class methods
    @classmethod
    def from_dict(cls, data: dict) -> 'FoodItem':
        """
        Factory method: create FoodItem from dictionary.
        
        Args:
            data: Dict containing food information
            
        Returns:
            FoodItem instance
        """
        return cls(
            name=data['name'],
            quantity=data['quantity'],
            unit=data['unit'],
            expiry_date=datetime.fromisoformat(data['expiry_date']),
            category=data.get('category', 'Other')
        )

    @classmethod
    def get_total_items(cls) -> int:
        """Return total number of food items created."""
        return cls._total_items

    # ✅ 7. Static methods
    @staticmethod
    def calculate_shelf_life(purchase_date: datetime, expiry_date: datetime) -> int:
        """
        Calculate shelf life (utility function).
        
        Args:
            purchase_date: Purchase date
            expiry_date: Expiration date
            
        Returns:
            Number of days
        """
        delta = expiry_date - purchase_date
        return delta.days

    # ✅ 8. Protected methods
    def _validate_expiry_date(self, date: datetime) -> bool:
        """Validate expiration date."""
        return date > datetime.now()

    # ✅ 9. Private methods
    def __log_usage(self, amount: float):
        """Log food usage (very private)."""
        pass
```

---

## 3. General Principles

### ✅ Don't Write Java-style Getters/Setters

❌ **Wrong** - Java style:
```python
class ShoppingList:
    def get_total_items(self):
        return self._total_items
    
    def set_total_items(self, value):
        self._total_items = value
```

✅ **Correct** - Pythonic style:
```python
class ShoppingList:
    @property
    def total_items(self) -> int:
        """Total number of items in list."""
        return len(self._items)
```

### ✅ Don't Overuse Double Underscore

Only override when truly needed:
- `__init__`, `__str__`, `__repr__`, `__eq__`, `__lt__`, `__len__`
- `__enter__`, `__exit__` (context manager)
- `__getitem__`, `__setitem__` (indexing)

### ✅ Prefer Composition Over Inheritance

❌ **Avoid** complex inheritance:
```python
class Food: pass
class PerishableFood(Food): pass
class Vegetable(PerishableFood): pass
class LeafyVegetable(Vegetable): pass
```

✅ **Use** composition when appropriate:
```python
class ExpiryTracker:
    """Track expiration dates."""
    def check_status(self, food_item: FoodItem) -> str:
        if food_item.is_expired:
            return "Expired"
        elif food_item.is_expiring_soon:
            return "Expiring Soon"
        return "Good"

class Refrigerator:
    def __init__(self):
        self.expiry_tracker = ExpiryTracker()  # Has-a relationship
        self._items: List[FoodItem] = []
```

---

## 4. Visibility

| Level | Notation | Purpose |
|-------|----------|---------|
| Public | `attribute` | Public API |
| Protected | `_attribute` | Internal use, subclasses |
| Private | `__attribute` | Avoid override, name mangling |

```python
class UserAccount:
    def __init__(self, username: str):
        self.username = username              # Public
        self._shopping_lists = []             # Protected
        self.__password_hash = "encrypted"    # Private (name mangling)
```

**Note**: Python doesn't have true private. `_` and `__` are conventions!

---

## 5. Comments & Docstrings

### Standard Docstring (Google Style)

```python
from typing import List
from datetime import datetime

class MealPlanner:
    """
    Manage meal plans for families.
    
    Attributes:
        user_id (str): User ID
        meal_plans (List[MealPlan]): List of meal plans
        MAX_PLANS_PER_WEEK (int): Maximum plans per week
    
    Example:
        >>> planner = MealPlanner("user123")
        >>> planner.create_weekly_plan(start_date=datetime.now())
    """

    MAX_PLANS_PER_WEEK = 21  # 3 meals/day * 7 days

    def suggest_recipes(
        self, 
        refrigerator: 'Refrigerator',
        min_ingredients: int = 3
    ) -> List[str]:
        """
        Suggest recipes based on fridge contents.
        
        Args:
            refrigerator: Refrigerator object containing food
            min_ingredients: Minimum ingredients required (default 3)
        
        Returns:
            List of recipe names that can be cooked
        
        Raises:
            ValueError: If min_ingredients < 1
            EmptyFridgeError: If refrigerator is empty
        
        Note:
            - Prioritizes recipes using soon-to-expire ingredients
        """
        if min_ingredients < 1:
            raise ValueError("Min ingredients must be >= 1")
        
        # TODO: Integrate AI for smarter suggestions
        # FIXME: Handle multiple items with same name but different units
        # NOTE: This feature will be expanded in v2.0
        
        return self._match_recipes(available_foods, min_ingredients)
```

---

## 6. Magic Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `__str__` | User-friendly string | `print(item)` |
| `__repr__` | Debug string | `repr(item)` |
| `__eq__`, `__lt__` | Comparison | `item1 == item2` |
| `__len__` | Length | `len(fridge)` |
| `__getitem__` | Indexing | `fridge[0]` |
| `__contains__` | Membership | `'Tomato' in fridge` |
| `__iter__` | Iterator | `for item in fridge:` |

```python
class ShoppingList:
    def __str__(self) -> str:
        return f"📝 List: {self.name}\n{items_str}"
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __getitem__(self, index: int) -> dict:
        return self._items[index]
    
    def __contains__(self, item_name: str) -> bool:
        return any(item['name'] == item_name for item in self._items)
    
    def __iter__(self):
        return iter(self._items)
```

---

## 7. Constants & Configuration

Write in UPPER_CASE:

```python
# config.py
DEFAULT_EXPIRY_WARNING_DAYS = 3
MAX_ITEMS_PER_SHOPPING_LIST = 100
MAX_STORAGE_DAYS = 365

FOOD_CATEGORIES = [
    "Vegetables",
    "Meat",
    "Dry Goods",
    "Beverages",
    "Other"
]

class SystemConfig:
    DATABASE_URL = "postgresql://localhost/shopping_system"
    CACHE_TIMEOUT = 300  # seconds
    MAX_CONCURRENT_USERS = 1000
```

**Don't hardcode in functions**:

❌ Wrong:
```python
def check_expiry(self, food_item):
    if food_item.days_until_expiry <= 3:  # Magic number!
        return "Expiring Soon"
```

✅ Correct:
```python
def check_expiry(self, food_item):
    if food_item.days_until_expiry <= DEFAULT_EXPIRY_WARNING_DAYS:
        return "Expiring Soon"
```

---

## 8. Code Organization

### Import Order (PEP 8):

```python
# 1. Standard library
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# 2. Third-party libraries
import requests
from sqlalchemy import create_engine

# 3. Internal project modules
from .models import FoodItem, Recipe
from .storage import Refrigerator
from .config import MAX_PLANS_PER_WEEK
```

### Class Member Order:
1. Class attributes
2. `__init__` constructor
3. Magic methods (`__str__`, `__repr__`, ...)
4. Properties (`@property`)
5. Public methods
6. Class methods (`@classmethod`)
7. Static methods (`@staticmethod`)
8. Protected methods (`_method`)
9. Private methods (`__method`)

## 9. Inheritance & Composition

### Proper Inheritance with ABC

```python
from abc import ABC, abstractmethod

class FoodStorage(ABC):
    """Abstract base class for food storage areas."""
    
    def __init__(self, name: str, capacity: int):
        self.name = name
        self.capacity = capacity
        self._items: List[FoodItem] = []
    
    @abstractmethod
    def add_item(self, item: FoodItem) -> bool:
        """Must be implemented in subclass."""
        pass
    
    @abstractmethod
    def get_optimal_temperature(self) -> float:
        """Optimal temperature for storage area."""
        pass
    
    def remove_expired_items(self) -> List[FoodItem]:
        """Common method for all storage types."""
        expired = [item for item in self._items if item.is_expired]
        self._items = [item for item in self._items if not item.is_expired]
        return expired

class RefrigeratorCompartment(FoodStorage):
    """Refrigerator compartment - cold storage."""
    
    def add_item(self, item: FoodItem) -> bool:
        if item.category not in ["Vegetables", "Meat", "Beverages"]:
            return False
        self._items.append(item)
        return True
    
    def get_optimal_temperature(self) -> float:
        return 4.0  # Celsius

class Pantry(FoodStorage):
    """Pantry - dry goods storage."""
    
    def add_item(self, item: FoodItem) -> bool:
        if item.category != "Dry Goods":
            return False
        self._items.append(item)
        return True
    
    def get_optimal_temperature(self) -> float:
        return 25.0  # Celsius
```

### Composition Over Inheritance

```python
class NotificationService:
    """Send notifications."""
    def send_expiry_alert(self, user_id: str, food_items: List[FoodItem]):
        message = f"You have {len(food_items)} items expiring soon!"
        print(f"[Notification to {user_id}] {message}")

class InventoryTracker:
    """Track food inventory."""
    def calculate_usage_rate(self, item: FoodItem, days: int = 7) -> float:
        return 0.5  # kg/day (example)
    
    def predict_restock_date(self, item: FoodItem) -> datetime:
        usage_rate = self.calculate_usage_rate(item)
        days_remaining = item.quantity / usage_rate if usage_rate > 0 else 999
        return datetime.now() + timedelta(days=int(days_remaining))

class SmartRefrigerator:
    """Smart refrigerator using composition."""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        # Has-a relationships
        self.main_compartment = RefrigeratorCompartment("Main")
        self.notification_service = NotificationService()
        self.inventory_tracker = InventoryTracker()
        self._all_items: List[FoodItem] = []
    
    def check_and_notify_expiry(self):
        expiring_soon = [item for item in self._all_items if item.is_expiring_soon]
        if expiring_soon:
            self.notification_service.send_expiry_alert(self.user_id, expiring_soon)
```

---

## 10. Advanced Best Practices

### Type Hints (PEP 484)

```python
from typing import List, Dict, Optional, Union, Tuple

class ShoppingListManager:
    def __init__(self):
        self.lists: Dict[str, ShoppingList] = {}
        self.history: List[Tuple[datetime, str]] = []
    
    def create_list(self, name: str, items: Optional[List[dict]] = None) -> ShoppingList:
        """Create a new shopping list."""
        new_list = ShoppingList(name)
        if items:
            for item in items:
                new_list.add_item(item)
        return new_list
    
    def get_list(self, name: str) -> Optional[ShoppingList]:
        """Get list by name, returns None if not found."""
        return self.lists.get(name)
```

### Context Managers

```python
class RefrigeratorSession:
    """Context manager for refrigerator sessions."""
    
    def __init__(self, fridge: 'Refrigerator', user_id: str):
        self.fridge = fridge
        self.user_id = user_id
        self.start_time = None
        self.changes_made = []
    
    def __enter__(self) -> 'RefrigeratorSession':
        self.start_time = datetime.now()
        print(f"[{self.user_id}] Opened fridge at {self.start_time}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()
        print(f"[{self.user_id}] Closed fridge after {duration:.1f}s")
        print(f"Made {len(self.changes_made)} changes")
        return False  # Don't suppress exceptions

# Usage
with RefrigeratorSession(fridge, "user123") as session:
    session.add_item(tomato)
    session.remove_item("old_item")
```

### Dataclasses (Python 3.7+)

```python
from dataclasses import dataclass, field

@dataclass
class ShoppingItem:
    """Shopping item using dataclass."""
    name: str
    quantity: float
    unit: str
    category: str = "Other"
    estimated_price: float = 0.0
    is_purchased: bool = False
    
    def mark_purchased(self):
        self.is_purchased = True
    
    def calculate_total_price(self) -> float:
        return self.quantity * self.estimated_price

# Auto-generates __init__, __repr__, __eq__
item = ShoppingItem(name="Tomato", quantity=2.0, unit="kg", estimated_price=15000)
```

---

## 11. SOLID Principles

### S - Single Responsibility Principle

```python
# ❌ Wrong - class has too many responsibilities
class FoodManager:
    def add_food(self, food): pass
    def send_notification(self, food): pass
    def save_to_database(self, food): pass
    def create_pdf_report(self): pass

# ✅ Correct - each class has one responsibility
class FoodRepository:
    """Only manages food storage in database."""
    def save(self, food: FoodItem): pass
    def find_by_id(self, food_id: str) -> Optional[FoodItem]: pass

class NotificationService:
    """Only manages notifications."""
    def send_expiry_alert(self, user_id: str, food: FoodItem): pass

class ReportGenerator:
    """Only generates reports."""
    def create_weekly_report(self, user_id: str) -> str: pass
```

### O - Open/Closed Principle

```python
# Open for extension, closed for modification

class PriceCalculator(ABC):
    @abstractmethod
    def calculate(self, base_price: float, quantity: float) -> float:
        pass

class StandardPriceCalculator(PriceCalculator):
    def calculate(self, base_price: float, quantity: float) -> float:
        return base_price * quantity

class BulkDiscountCalculator(PriceCalculator):
    def __init__(self, threshold: float, discount_percent: float):
        self.threshold = threshold
        self.discount_percent = discount_percent
    
    def calculate(self, base_price: float, quantity: float) -> float:
        total = base_price * quantity
        if quantity >= self.threshold:
            total *= (1 - self.discount_percent / 100)
        return total

# Extend by adding new calculators, not modifying existing code
```

### L - Liskov Substitution Principle

```python
# Subclass must be substitutable for base class

class Storage(ABC):
    @abstractmethod
    def can_store(self, item: FoodItem) -> bool:
        pass
    
    @abstractmethod
    def add_item(self, item: FoodItem) -> bool:
        pass

class ColdStorage(Storage):
    def can_store(self, item: FoodItem) -> bool:
        return item.category in ["Vegetables", "Meat"]
    
    def add_item(self, item: FoodItem) -> bool:
        if self.can_store(item):
            self._items.append(item)
            return True
        return False

# Any Storage subclass works with this function
def store_items(storage: Storage, items: List[FoodItem]):
    for item in items:
        storage.add_item(item)
```

### I - Interface Segregation Principle

```python
# Don't force clients to implement unnecessary methods

# ✅ Correct - separate small interfaces
class FoodOperations(ABC):
    @abstractmethod
    def add_food(self, food: FoodItem) -> bool: pass
    @abstractmethod
    def remove_food(self, food_id: str) -> bool: pass

class ExpiryChecker(ABC):
    @abstractmethod
    def check_expiry(self, food: FoodItem) -> str: pass

class ReportGenerator(ABC):
    @abstractmethod
    def generate_report(self) -> dict: pass

# Class only implements what it needs
class BasicStorage(FoodOperations):
    # Only implements CRUD, not reports or expiry checks
    pass

class SmartStorage(FoodOperations, ExpiryChecker):
    # Implements both interfaces
    pass
```

### D - Dependency Inversion Principle

```python
# Depend on abstractions, not concrete implementations

# ✅ Correct - depend on abstraction
class Database(ABC):
    @abstractmethod
    def save(self, data: dict) -> bool: pass

class PostgreSQLDatabase(Database):
    def save(self, data: dict) -> bool:
        print(f"Saving to PostgreSQL: {data}")
        return True

class MongoDBDatabase(Database):
    def save(self, data: dict) -> bool:
        print(f"Saving to MongoDB: {data}")
        return True

class FoodManager:
    def __init__(self, database: Database):  # Depend on abstraction
        self.database = database
    
    def save_food(self, food: FoodItem) -> bool:
        data = {'name': food.name, 'quantity': food.quantity}
        return self.database.save(data)

# Dependency injection - inject database in constructor
manager1 = FoodManager(PostgreSQLDatabase())
manager2 = FoodManager(MongoDBDatabase())
```
## 12. Review Checklist

### Naming & Style
- [ ] Class names in **PascalCase**
- [ ] Method/attribute names in **snake_case**
- [ ] Constants in **UPPER_CASE**
- [ ] Private/protected attributes have `_` or `__` prefix
- [ ] Class names are nouns, method names are verbs

### Documentation
- [ ] **Docstrings** for classes and public methods
- [ ] Docstrings follow standard format (Google/NumPy)
- [ ] Type hints for parameters and return values
- [ ] Comments explain complex logic
- [ ] Usage examples in docstrings (when needed)

### Structure
- [ ] Class members in correct order
- [ ] Imports organized per PEP 8
- [ ] No duplicate code
- [ ] Methods are concise (<50 lines)
- [ ] File names use snake_case

### OOP Principles
- [ ] Single Responsibility - one responsibility per class
- [ ] Use `@property` instead of getter/setter
- [ ] Magic methods properly implemented
- [ ] Inheritance used correctly (IS-A relationship)
- [ ] Composition preferred when appropriate (HAS-A)
- [ ] Follows SOLID principles

### Quality & Testing
- [ ] No hardcoded values - use constants
- [ ] Error handling properly implemented
- [ ] Code follows PEP 8 (use `black`, `flake8`)
- [ ] Input validation included
- [ ] Business logic meets system requirements