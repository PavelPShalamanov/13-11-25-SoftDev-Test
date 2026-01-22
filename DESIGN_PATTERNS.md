# Често срещани принципи за дизайн

## 1. Factory method

Фабричният метод е генераторен принцип за дизайн, който дефинира интерфейс за създаване на обекти, като позволява на подкласовете да определят конкретния тип на създавания обект. Така логиката за създаване се отделя от логиката за използване на обекта, което намалява зависимостите между класовете.

## 2. Strategy

Стратегиите са поведенчески принцип, който създава един главен контекст за изпълнение на логика и много отделни обекти дефиниращи конкретни алгоритми. Контекстът разполага единствено с информацията която трябва да бъде обработена и връзка към конкретна стратегия на която може да бъде предадена тя. Стратегиите са имплементации на един общ интерфейс, но се различават по алгоритмите, които изпълняват.

## 3. State

Състоянията са поведенчески принцип, който позволява промяната на поведението на даден обект при изпълнението на конкретни условия. Всяко състояние дефинира принцип на работа, а обектът дефинира връзките между различните състояния и преходите между тях. Така един обек може да изпълнява различни действия в зависимост от контекста в който се намира.

## 4. Observer

Наблюдателите са поведенчески принцип, който позволява на много отделни обекти да следят събития, излъчвани от един конкретен обект. Този обект притежава връзки към всички негови последователи, като уведомявайки ги за случилото се събитие в конкретен момент предизвиква изпълнението на вътрешна логика във всеки един от тях.

## 5. Пример за Strategy

Декларация на абстрактен клас за стратегия:

```python
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass
```

Дефиниция на конкретни стратегии:

```python
class CreditCardPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Paying {amount} using Credit Card")


class PayPalPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Paying {amount} using PayPal")


class CryptoPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Paying {amount} using Cryptocurrency")
```

контекст, управяляващ стратегиите:

```python
class PaymentContext:
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def execute_payment(self, amount: float):
        self._strategy.pay(amount)
```

използване:

```python
context = PaymentContext(CreditCardPayment())
context.execute_payment(100)

context.set_strategy(PayPalPayment())
context.execute_payment(50)

context.set_strategy(CryptoPayment())
context.execute_payment(200)
```

Изход:

```python
Paying 100 using Credit Card
Paying 50 using PayPal
Paying 200 using Cryptocurrency
```
