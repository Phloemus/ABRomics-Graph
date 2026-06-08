jq '
[
  .results.bindings
  | to_entries[]
  | {
      model: "constant_data.source",
      pk: (.key + 1),
      fields: {
        name: .value.classLabel.value,
        type: "food",
        class: .value.class.value,
        ontology: "FOODON"
      }
    }
]
' query-result.json > output.json
