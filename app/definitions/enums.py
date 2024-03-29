from enum import Enum


class TaskState(str, Enum):
	PENDING = 'pending'
	RUNNING = 'running'
	FINISHED = 'finished'
	FAILED = 'failed'


class LogTypes(str, Enum):
	SDK = 'SDK'
	STUB = 'STUB'


class SupportedLanguages(str, Enum):
	ActionScript = 'ActionScript'
	Ada = 'Ada'
	Apex = 'Apex'
	Bash = 'Bash'
	C = 'C'
	C_PLUS_PLUS = ' C++'
	C_SHARP = 'C#'
	Clojure = 'Clojure'
	Crystal = 'Crystal'
	Dart = 'Dart'
	Elixir = 'Elixir'
	Elm = 'Elm'
	Eiffel = 'Eiffel'
	Erlang = 'Erlang'
	Go = 'Go'
	Groovy = 'Groovy'
	Haskell = 'Haskell'
	Java = 'Java'
	K6 = 'K6'
	Kotlin = 'Kotlin'
	Lua = 'Lua'
	Nim = 'NI'
	NodeJsJavaScript = 'Node.js/JavaScript'
	ObjectiveC = 'Objective-C'
	OCaml = 'OCaml'
	Perl = 'Perl'
	PHP = 'PHP'
	PowerShell = 'PowerShell'
	Python = 'Python'
	R = 'R'
	Ruby = 'Ruby'
	Rust = 'Rust'
	Scala = 'Scala'
	Swift = 'Swift'
	Typescript = 'Typescript'


class SupportedFrameworks(str, Enum):
	C_PLUS_PLUS = ' C++'
	C_SHARP = 'C#'
	ADA = 'Ada'
	ERLANG = 'Erlang'
	F_SHARP = 'F#'
	GO = 'Go'
	Haskell = 'Haskell'
	Java = 'Java'
	Kotlin = 'Kotlin'
	PHP = 'PHP'
	Python = 'Python'
	NodeJS = 'NodeJS'
	Ruby = 'Ruby'
	Rust = 'Rust'
	Scala = 'Scala'
