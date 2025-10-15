# Python OOP Conventions - Quy ước lập trình hướng đối tượng

## 📋 Mục lục
1. [Quy tắc đặt tên](#quy-tắc-đặt-tên)
2. [Cấu trúc Class](#cấu-trúc-class)
3. [Properties và Methods](#properties-và-methods)
4. [Inheritance và Composition](#inheritance-và-composition)
5. [Design Patterns phổ biến](#design-patterns-phổ-biến)
6. [Best Practices](#best-practices)

---

## 🏷️ Quy tắc đặt tên

### Classes
- Sử dụng **PascalCase** (CapWords)
- Tên class nên là danh từ hoặc cụm danh từ
- Tránh tiền tố/hậu tố không cần thiết

```python
# ✅ Đúng
class UserAccount:
    pass

class PaymentProcessor:
    pass

class DatabaseConnection:
    pass

# ❌ Sai
class user_account:  # Nên dùng PascalCase
    pass

class MyClass:  # Tên quá chung chung
    pass
```

### Methods và Instance Variables
- Sử dụng **snake_case**
- Method names nên là động từ hoặc cụm động từ

```python
class User:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self._password = None  # Protected
        self.__secret_key = None  # Private
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def set_password(self, password):
        self._password = self._hash_password(password)
    
    def _hash_password(self, password):  # Protected method
        return hash(password)
```

### Quy ước về visibility
- `public`: Không có tiền tố - `self.name`
- `protected`: Một dấu gạch dưới - `self._internal_value`
- `private`: Hai dấu gạch dưới - `self.__private_data`

---

## 🏗️ Cấu trúc Class

### Thứ tự các thành phần trong class

```python
class Product:
    """
    Đại diện cho một sản phẩm trong hệ thống.
    
    Attributes:
        name (str): Tên sản phẩm
        price (float): Giá sản phẩm
    """
    
    # 1. Class variables
    tax_rate = 0.1
    _instance_count = 0
    
    # 2. Constructor
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price
        Product._instance_count += 1
    
    # 3. Special methods (dunder methods)
    def __str__(self) -> str:
        return f"Product({self.name}, ${self.price})"
    
    def __repr__(self) -> str:
        return f"Product(name={self.name!r}, price={self.price})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.name == other.name and self.price == other.price
    
    # 4. Properties
    @property
    def final_price(self) -> float:
        """Tính giá cuối cùng bao gồm thuế."""
        return self.price * (1 + self.tax_rate)
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("Tên sản phẩm không được rỗng")
        self._name = value
    
    # 5. Public methods
    def apply_discount(self, percentage: float) -> None:
        """Áp dụng giảm giá cho sản phẩm."""
        if 0 <= percentage <= 100:
            self.price *= (1 - percentage / 100)
    
    # 6. Class methods
    @classmethod
    def get_instance_count(cls) -> int:
        """Trả về số lượng instance đã tạo."""
        return cls._instance_count
    
    # 7. Static methods
    @staticmethod
    def validate_price(price: float) -> bool:
        """Kiểm tra giá có hợp lệ không."""
        return price > 0
    
    # 8. Protected/Private methods
    def _calculate_tax(self) -> float:
        return self.price * self.tax_rate
```

---

## 🔧 Properties và Methods

### Sử dụng @property cho computed attributes

```python
class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    @property
    def area(self) -> float:
        """Diện tích hình chữ nhật."""
        return self.width * self.height
    
    @property
    def perimeter(self) -> float:
        """Chu vi hình chữ nhật."""
        return 2 * (self.width + self.height)
```

### Class methods vs Static methods

```python
class DateTime:
    def __init__(self, year: int, month: int, day: int):
        self.year = year
        self.month = month
        self.day = day
    
    @classmethod
    def from_string(cls, date_string: str):
        """Factory method - tạo instance từ string."""
        year, month, day = map(int, date_string.split('-'))
        return cls(year, month, day)
    
    @classmethod
    def today(cls):
        """Factory method - tạo instance với ngày hiện tại."""
        import datetime
        today = datetime.date.today()
        return cls(today.year, today.month, today.day)
    
    @staticmethod
    def is_leap_year(year: int) -> bool:
        """Utility method - không cần class hay instance."""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

---

## 🧬 Inheritance và Composition

### Inheritance đúng cách

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    """Base class trừu tượng cho động vật."""
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    @abstractmethod
    def make_sound(self) -> str:
        """Method trừu tượng bắt buộc implement."""
        pass
    
    def eat(self) -> str:
        return f"{self.name} đang ăn"

class Dog(Animal):
    def __init__(self, name: str, age: int, breed: str):
        super().__init__(name, age)
        self.breed = breed
    
    def make_sound(self) -> str:
        return "Gâu gâu!"
    
    def fetch(self) -> str:
        return f"{self.name} đang nhặt bóng"

class Cat(Animal):
    def make_sound(self) -> str:
        return "Meo meo!"
    
    def scratch(self) -> str:
        return f"{self.name} đang cào"
```

### Composition over Inheritance

```python
class Engine:
    def __init__(self, horsepower: int):
        self.horsepower = horsepower
    
    def start(self) -> str:
        return "Engine started"

class Wheels:
    def __init__(self, count: int):
        self.count = count
    
    def rotate(self) -> str:
        return f"{self.count} wheels rotating"

# ✅ Sử dụng Composition
class Car:
    def __init__(self, engine: Engine, wheels: Wheels):
        self.engine = engine  # Has-a relationship
        self.wheels = wheels  # Has-a relationship
    
    def drive(self) -> str:
        return f"{self.engine.start()}, {self.wheels.rotate()}"

# Sử dụng
engine = Engine(200)
wheels = Wheels(4)
car = Car(engine, wheels)
```

### Multiple Inheritance và MRO (Method Resolution Order)

```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):  # Diamond problem
    pass

# Kiểm tra MRO
print(D.mro())  # [D, B, C, A, object]
d = D()
print(d.method())  # "B" - theo thứ tự MRO
```

---

## 🎨 Design Patterns phổ biến

### 1. Singleton Pattern

```python
class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.connection = "Connected to DB"

# Sử dụng
db1 = DatabaseConnection()
db2 = DatabaseConnection()
print(db1 is db2)  # True
```

### 2. Factory Pattern

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def get_type(self) -> str:
        pass

class Car(Vehicle):
    def get_type(self) -> str:
        return "Car"

class Motorcycle(Vehicle):
    def get_type(self) -> str:
        return "Motorcycle"

class VehicleFactory:
    @staticmethod
    def create_vehicle(vehicle_type: str) -> Vehicle:
        if vehicle_type == "car":
            return Car()
        elif vehicle_type == "motorcycle":
            return Motorcycle()
        else:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")

# Sử dụng
vehicle = VehicleFactory.create_vehicle("car")
print(vehicle.get_type())
```

### 3. Observer Pattern

```python
from typing import List

class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

class Subject:
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        self._observers.append(observer)
    
    def detach(self, observer: Observer):
        self._observers.remove(observer)
    
    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)

class EmailNotifier(Observer):
    def update(self, message: str):
        print(f"Email sent: {message}")

class SMSNotifier(Observer):
    def update(self, message: str):
        print(f"SMS sent: {message}")

# Sử dụng
subject = Subject()
subject.attach(EmailNotifier())
subject.attach(SMSNotifier())
subject.notify("New order received!")
```

---

## ✨ Best Practices

### 1. Type Hints

```python
from typing import List, Dict, Optional, Union

class UserManager:
    def __init__(self):
        self.users: Dict[int, str] = {}
    
    def add_user(self, user_id: int, name: str) -> None:
        self.users[user_id] = name
    
    def get_user(self, user_id: int) -> Optional[str]:
        return self.users.get(user_id)
    
    def get_all_users(self) -> List[str]:
        return list(self.users.values())
```

### 2. Docstrings

```python
class Calculator:
    """
    Một calculator đơn giản cho các phép toán cơ bản.
    
    Attributes:
        history (list): Lịch sử các phép tính đã thực hiện
    
    Examples:
        >>> calc = Calculator()
        >>> calc.add(2, 3)
        5
    """
    
    def add(self, a: float, b: float) -> float:
        """
        Cộng hai số.
        
        Args:
            a: Số thứ nhất
            b: Số thứ hai
        
        Returns:
            Tổng của a và b
        
        Raises:
            TypeError: Nếu a hoặc b không phải là số
        """
        return a + b
```

### 3. Context Managers

```python
class FileManager:
    def __init__(self, filename: str, mode: str):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

# Sử dụng
with FileManager('data.txt', 'w') as f:
    f.write('Hello World')
```

### 4. Dataclasses (Python 3.7+)

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Student:
    name: str
    age: int
    grades: List[float] = field(default_factory=list)
    
    def average_grade(self) -> float:
        return sum(self.grades) / len(self.grades) if self.grades else 0.0

# Tự động tạo __init__, __repr__, __eq__
student = Student("John", 20, [8.5, 9.0, 7.5])
print(student)  # Student(name='John', age=20, grades=[8.5, 9.0, 7.5])
```

### 5. SOLID Principles

#### Single Responsibility Principle
```python
# ❌ Sai - Class có quá nhiều trách nhiệm
class User:
    def save_to_database(self): pass
    def send_email(self): pass
    def generate_report(self): pass

# ✅ Đúng - Mỗi class một trách nhiệm
class User:
    def __init__(self, name: str):
        self.name = name

class UserRepository:
    def save(self, user: User): pass

class EmailService:
    def send(self, user: User): pass
```

#### Open/Closed Principle
```python
from abc import ABC, abstractmethod

class Discount(ABC):
    @abstractmethod
    def calculate(self, price: float) -> float:
        pass

class PercentageDiscount(Discount):
    def __init__(self, percentage: float):
        self.percentage = percentage
    
    def calculate(self, price: float) -> float:
        return price * (1 - self.percentage / 100)

class FixedDiscount(Discount):
    def __init__(self, amount: float):
        self.amount = amount
    
    def calculate(self, price: float) -> float:
        return max(0, price - self.amount)
```

---

## 📝 Checklist cho Code Review

- [ ] Class names sử dụng PascalCase
- [ ] Method names sử dụng snake_case
- [ ] Có docstring cho class và public methods
- [ ] Sử dụng type hints cho parameters và return values
- [ ] Properties được sử dụng cho computed attributes
- [ ] Không có God class (class quá lớn với quá nhiều trách nhiệm)
- [ ] Inheritance được sử dụng đúng cách (IS-A relationship)
- [ ] Composition được ưu tiên khi phù hợp (HAS-A relationship)
- [ ] Special methods (`__str__`, `__repr__`, `__eq__`) được implement khi cần
- [ ] Error handling được xử lý đúng cách

---

## 🔗 Tài liệu tham khảo

- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Python Official Documentation - Classes](https://docs.python.org/3/tutorial/classes.html)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

---

**Lưu ý:** Đây là các quy ước phổ biến nhất. Team có thể điều chỉnh cho phù hợp với dự án cụ thể, nhưng quan trọng nhất là **nhất quán** trong toàn bộ codebase.