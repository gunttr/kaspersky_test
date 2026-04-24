# Инструкция по развертыванию микросервиса

## Требования

- Виртуальная машина с установленной ОС (Использовался Rocky Linux 10 Minimal)
- Настроенный SSH доступ к ВМ
- Установленный Ansible на управляющей машине
- Установленный Docker на ВМ
- Пользователь с правами sudo (желатльно без запроса пароля / NOPASSWD)

Дополнительно (опционально):

- Проброшенные порты:
    - 8080 - микросервис
    - 9080 - Prometheus
    - 9100 - Node Exporter

---

## Настройка Ansible

Отредактируйте файл `inventory.ini` в соответствии с вашей конфигурацией.

Пример:

```ini
[servers]
rocky_linux_vm_ansible
```

---

## Деплой микросервиса

### Локальный запуск

```bash
ansible-playbook -i inventory.ini playbook.yaml
```

или

```bash
ansible-playbook -i inventory.ini playbook.yaml -e microservice_mode=local
```

### Запуск в Docker контейнере

```bash
ansible-playbook -i inventory.ini playbook.yaml -e microservice_mode=container
```

---

## Проверка

На виртуальной машине в браузере (или с хоста, если проброшены порты):

- [Микросервис](http://localhost:8080)
- [Prometheus](http://localhost:9080)
- [Node Exporter](http://localhost:9100)
