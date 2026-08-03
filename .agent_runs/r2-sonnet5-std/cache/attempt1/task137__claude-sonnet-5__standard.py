import io
import tokenize


def find_markers(source):
    results = []
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for tok in tokens:
            if tok.type == tokenize.COMMENT:
                text = tok.string
                idx_todo = text.find("TODO")
                idx_fixme = text.find("FIXME")
                candidates = [(i, m) for i, m in ((idx_todo, "TODO"), (idx_fixme, "FIXME")) if i != -1]
                if candidates:
                    candidates.sort(key=lambda x: x[0])
                    results.append((tok.start[0], candidates[0][1]))
    except tokenize.TokenizeError:
        pass
    except (IndentationError, SyntaxError):
        pass
    except Exception:
        pass
    return results
