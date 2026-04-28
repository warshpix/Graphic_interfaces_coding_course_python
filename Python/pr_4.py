# 1. Ієрархія винятків
class TransactionError(Exception):
    pass

class InsufficientFundsError(TransactionError):
    def __init__(self, balance, amount):
        super().__init__(f"Недостатньо коштів на рахунку! Поточний баланс: {balance}")

class InvalidAmountError(TransactionError):
    def __init__(self):
        super().__init__("Сума операції повинна бути більшою за нуль!")

class AuthError(Exception):
    """Помилка доступу: гаманець заблоковано"""
    pass


# 2. Декоратори (окремі функції)
def log_operation(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG]: Виконується операція {func.__name__} з аргументами {args[1:]}")
        return func(*args, **kwargs)
    return wrapper

def require_unlocked(func):
    def wrapper(self, *args, **kwargs):
        if not self.is_unlocked:
            raise AuthError("Операція відхилена: гаманець заблоковано!")
        return func(self, *args, **kwargs)
    return wrapper

# 3. Клас EWallet
class EWallet:
    def __init__(self, owner):
        self.owner = owner
        self._balance = 0
        self.is_unlocked = False

    def unlock(self):
        print("Розблокування гаманця...")
        self.is_unlocked = True

    def lock(self):
        self.is_unlocked = False

    @log_operation
    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError()
        self._balance += amount
        print(f"Баланс поповнено. Поточний баланс: {self._balance}")

    @log_operation
    @require_unlocked
    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError()
        if amount > self._balance:
            raise InsufficientFundsError(self._balance, amount)
        self._balance -= amount
        print(f"Успішно знято {amount}. Залишок: {self._balance}")

# 4. Сценарій використання (ваш "Main")
if __name__ == "__main__":
    wallet = EWallet("User")
    print(f"Гаманець створено для користувача: {wallet.owner}")

    # Спроба зняти кошти з заблокованого гаманця
    try:
        print("Спроба зняти кошти з заблокованого гаманця...")
        wallet.withdraw(100)
    except AuthError as e:
        print(f"Помилка доступу: {e}")

    wallet.unlock()

    # Поповнення
    try:
        wallet.deposit(500)
    except TransactionError as e:
        print(f"Помилка транзакції: {e}")

    # Спроба зняти забагато
    try:
        wallet.withdraw(600)
    except TransactionError as e:
        print(f"Помилка транзакції: {e}")

    # Від'ємна сума
    try:
        wallet.deposit(-50)
    except TransactionError as e:
        print(f"Помилка транзакції: {e}")