import ast
import re

def get_exp(area, is_boss, is_super_boss, name):
    if is_super_boss:
        return 8000000000, 10000000000
    if is_boss:
        if name == "Goblin King":
            return 250, 500
        elif name == "Skeleton King":
            return 250, 500
        else:
            base_min = 250
            base_max = 500
            scale = 1.5 ** (area - 1)
            return int(base_min * scale), int(base_max * scale)
    else:
        base_min = 10
        base_max = 25
        scale = 1.5 ** (area - 1)
        return int(base_min * scale), int(base_max * scale)

# Parse the AST to find and modify MONSTERS
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

tree = ast.parse(content, filename='app.py')

class MonsterUpdater(ast.NodeTransformer):
    def visit_Assign(self, node):
        if (len(node.targets) == 1 and
            isinstance(node.targets[0], ast.Name) and
            node.targets[0].id == 'MONSTERS' and
            isinstance(node.value, ast.List)):
            new_elts = []
            for elt in node.value.elts:
                if isinstance(elt, ast.Dict):
                    # Add exp_min and exp_max
                    m_dict = {}
                    for key, value in zip(elt.keys, elt.values):
                        if isinstance(key, ast.Constant):
                            k = key.value
                            if isinstance(value, ast.Constant):
                                v = value.value
                            elif isinstance(value, ast.Dict):
                                # Handle drop dict
                                drop = {}
                                for dk, dv in zip(value.keys, value.values):
                                    if isinstance(dk, ast.Constant):
                                        dk_val = dk.value
                                    if isinstance(dv, ast.Constant):
                                        dv_val = dv.value
                                    elif isinstance(dv, ast.Num):
                                        dv_val = dv.n
                                    drop[dk_val] = dv_val
                                v = drop
                            else:
                                continue  # Skip complex values
                            m_dict[k] = v
                    area = m_dict.get('area', 1)
                    is_boss = m_dict.get('is_boss', False)
                    is_super_boss = m_dict.get('is_super_boss', False)
                    name = m_dict.get('name', '')
                    exp_min, exp_max = get_exp(area, is_boss, is_super_boss, name)
                    m_dict['exp_min'] = exp_min
                    m_dict['exp_max'] = exp_max
                    # Rebuild the dict node
                    keys = [ast.Constant(k) for k in m_dict.keys()]
                    values = []
                    for v in m_dict.values():
                        if isinstance(v, int):
                            values.append(ast.Constant(v))
                        elif isinstance(v, str):
                            values.append(ast.Constant(v))
                        elif isinstance(v, bool):
                            values.append(ast.NameConstant(v))
                        elif isinstance(v, dict):
                            # Rebuild drop dict
                            d_keys = [ast.Constant(dk) for dk in v.keys()]
                            d_values = [ast.Constant(dv) if isinstance(dv, (int, float, str)) else ast.Constant(dv) for dv in v.values()]
                            values.append(ast.Dict(keys=d_keys, values=d_values))
                        else:
                            values.append(ast.Constant(v))
                    new_elts.append(ast.Dict(keys=keys, values=values))
            node.value.elts = new_elts
        return self.generic_visit(node)

transformer = MonsterUpdater()
new_tree = transformer.visit(tree)

# Write back
new_content = ast.unparse(new_tree)
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated MONSTERS")