import flask
from flask import request, jsonify, g, json, Response

from .. import application
from .. import db
from ..models import Solutions


@application.route('/api/v1/solutions/search', methods=['POST'])
def search():
    sub_industry = request.json.get('sub_industry')
    available_sols = Solutions.query.filter_by(sub_industry=sub_industry).all()
    print(available_sols[1].contact_details)
    solutions_list = []
    for solution in available_sols:
        sol_obj = {
            "name": solution.name,
            "details": solution.details,
            "best_for": solution.best_for,
            "contact_details": solution.contact_details
        }
        solutions_list.append(sol_obj)

    return jsonify(results=solutions_list)


@application.route('/api/v1/solutions/populate', methods=['POST'])
def populate():
    name = request.json.get('name')
    sector = request.json.get('sector')
    industry = request.json.get('industry')
    industry_group = request.json.get('industry_group')
    sub_industry = request.json.get('sub_industry')
    details = request.json.get('details')
    best_for = request.json.get('best_for')
    contact_details = request.json.get('contact_details')

    print(contact_details)

    if not name or not sector or not industry or not industry_group or not sub_industry or not details or not best_for or not contact_details:
        return jsonify({"Message": "All fields are required."})
    solution = Solutions(name=name, sector=sector, industry=industry, industry_group=industry_group,
                         sub_industry=sub_industry, details=details, best_for=best_for, contact_details=contact_details)
    db.session.add(solution)
    db.session.commit()
    return jsonify({"Message": "Solution added successfully."})
