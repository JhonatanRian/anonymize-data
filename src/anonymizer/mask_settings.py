from dataclasses import dataclass, field


@dataclass(slots=True)
class StringMaskSettings:
    size_anonymization: float = field(default=0.7)

    def __post_init__(self):
        self.size_anonymization = round(self.size_anonymization, 1)

        if not (0 <= self.size_anonymization <= 1):
            raise ValueError("O campo 'size_anonymization' deve estar entre 0 e 1.")

