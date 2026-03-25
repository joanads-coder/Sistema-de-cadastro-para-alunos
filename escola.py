from database import datebase # type: ignore
escola = datebase("escola.db")
alunos: list[str]= ["joana"
", dayanny, jonas,"]
notas: tuple[float, float, float]= (1.0, 10.0, 9.0)
print("alunos: ", alunos)
print("notas: ", notas)

def cadastrar_aluno(nome: str, nota: float) -> None:
    escola.cadastrar_aluno(nome, nota)
    def listar_alunos() -> list[tuple[str, float]]:
        return escola.listar_alunos()
    def calcular_media() -> float:
        return escola.calcular_media()
    def calcular_aprovacao() -> str:
        return escola.calcular_aprovacao()
    cadastrar_aluno("joana", 1.0)
    cadastrar_aluno("dayanny", 10.0)
    cadastrar_aluno("jonas", 9.0)
    print("alunos cadastrados: ", listar_alunos())
    print("média das notas: ", calcular_media())
    print("resultado da aprovação: ", calcular_aprovacao())
    







