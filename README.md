# Dick语言

Dick是一种简单而强大的脚本语言，旨在提供一种轻量级的编程体验，支持基本的控制流、变量操作和SQL数据库交互。

## 目录结构

```
OperateSys/
├── main.py          # 语言解释器入口
├── error.py         # 错误处理模块
├── libs/            # 核心库
│   └── Handle/      # 处理模块
│       ├── handle.py    # 关键字和函数处理
│       └── Expr/        # 表达式处理
│           ├── expr.py      # 表达式计算
│           └── SQL/         # SQL操作
│               └── sql.py   # SQL处理实现
└── example/         # 示例脚本
    ├── script.dick      # 基本示例
    ├── string.dick      # 字符串操作示例
    └── twoif.dick       # 条件语句示例
```

## 语言特性

### 数据类型
- `int`: 整数类型
- `str`: 字符串类型
- `float`: 浮点数类型
- `bool`: 布尔类型（true/false）

### 关键字
- `if`: 条件语句
- `while`: 循环语句
- `end`: 结束语句块

### 运算符
- 算术运算符: `+`, `-`, `*`, `/`
- 比较运算符: `>`, `<`, `>=`, `<=`, `==`, `!=`

### 标准函数
- `print`: 输出内容到控制台

### 特殊操作符
- `->`: 调用库函数，如 `->sql.Conn` 或 `->toChar`

### 注释
- 行注释: `# 这是注释`
- 行内注释: `x = 1 # 这是行内注释`

## 基本语法

### 变量定义与赋值

```dick
# 定义变量并指定类型
x: int = 10

# 直接赋值（类型推断）
y = 20

# 字符串变量
s: str = "Hello, Dick!"
```

### 条件语句

```dick
if x > y
    print x
end

if x == y
    print "x equals y"
end
```

### 循环语句

```dick
x: int = 0
while x < 10
    print x
    x = x + 1
end
```

### 表达式计算

```dick
# 算术运算
result = 10 + 5 * 2

# 字符串连接
message = "Hello" + " " + "World"

# 类型转换
char = 65 -> toChar  # 转换为字符 'A'
order = 'A' -> toOrder  # 转换为ASCII码 65
```

## 库功能

### SQL库

Dick语言内置了SQL库，支持与SQLite数据库的交互。

#### 用法示例

```dick
# 连接到数据库
"test.db" -> sql.Conn

# 创建表
"CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)" -> sql.Execute

# 插入数据
"INSERT INTO users (name, age) VALUES ('Alice', 30)" -> sql.Execute
"INSERT INTO users (name, age) VALUES ('Bob', 25)" -> sql.Execute

# 提交事务
"" -> sql.Commit

# 查询数据
"SELECT * FROM users" -> sql.Execute

# 获取所有结果
result = "" -> sql.Fetchall
print result

# 关闭连接
"" -> sql.Close
```

## 运行Dick脚本

使用Python运行Dick脚本：

```bash
python main.py example/script.dick
```

## 示例

### 基本示例 (script.dick)

```dick
# 变量定义
x: int = 10
y: int = 20

# 条件语句
if x > y
    print "x is greater than y"
end

if x < y
    print "x is less than y"
end

# 循环语句
counter: int = 0
while counter < 5
    print counter
    counter = counter + 1
end
```

### 字符串操作示例 (string.dick)

```dick
# 字符串定义
greeting: str = "Hello"
name: str = "Dick"

# 字符串连接
message = greeting + " " + name + "!"
print message

# 类型转换
number: int = 42
text = number -> toChar
print "Number as string: " + text
```

### 条件语句示例 (twoif.dick)

```dick
# 嵌套条件语句
a: int = 10
b: int = 20

if a < b
    print "a is less than b"
    if a == 10
        print "a is exactly 10"
    end
end

print "Done"
```

## 错误处理

Dick语言提供了基本的错误处理机制，会在遇到语法错误、运行时错误或SQL错误时给出明确的错误信息。

## 未来计划

- 添加更多数据类型支持
- 增加更多标准库函数
- 支持函数定义和调用
- 改进错误处理机制
- 添加更多数据库类型支持

## 贡献

欢迎对Dick语言进行贡献，无论是修复bug还是添加新功能。

## 许可证

MIT License
