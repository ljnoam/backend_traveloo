def parse_flights(data):
    results = []
    proposals = [item.get("proposals", []) for item in data if "proposals" in item]
    gates_info = {}
    for item in data:
        if "gates_info" in item:
            gates_info.update(item["gates_info"])

    for proposal_group in proposals:
        for proposal in proposal_group:
            try:
                terms_key = next(iter(proposal["terms"]))
                terms = proposal["terms"][terms_key]
                segment = proposal["segment"]

                departure = segment[0]["flight"][0]
                arrival = segment[-1]["flight"][-1]

                airline = departure.get("marketing_carrier")
                price = terms.get("price")
                duration = proposal.get("total_duration")
                stops = len(segment) - 1
                departure_time = departure.get("departure_time")
                arrival_time = arrival.get("arrival_time")
                booking_link = terms.get("url")

                baggage = terms.get("flights_baggage", [[]])[0]
                handbags = terms.get("flights_handbags", [[]])[0]

                stopovers = []
                for seg in segment:
                    flights = seg.get("flight", [])
                    if len(flights) > 1:
                        for i in range(1, len(flights)):
                            stop = flights[i]
                            prev = flights[i-1]
                            stopovers.append({
                                "stop_airport": stop.get("departure"),
                                "duration_minutes": stop.get("departure_timestamp", 0) - prev.get("arrival_timestamp", 0)
                            })

                flight_numbers = [f.get("number") for s in segment for f in s.get("flight", [])]
                aircrafts = [f.get("equipment") for s in segment for f in s.get("flight", [])]

                gate_info = gates_info.get(str(terms_key), {})
                payment_methods = gate_info.get("payment_methods", [])

                results.append({
                    "airline": airline,
                    "price": price,
                    "duration": duration,
                    "stops": stops,
                    "departure_time": departure_time,
                    "arrival_time": arrival_time,
                    "booking_link": booking_link,
                    "handbags": handbags,
                    "baggage": baggage,
                    "stopovers": stopovers,
                    "flight_numbers": flight_numbers,
                    "aircrafts": aircrafts,
                    "payment_methods": payment_methods,
                })
            except Exception:
                continue
    return results
