async def whois(whose) -> str:
    if whose == 'personal':
        whose = 'sched_user'
    elif whose == 'general':
        whose = 'sched_group'
    elif whose == 'arhit':
        whose = 'sched_arhit'
    else:
        raise ValueError
    return whose
