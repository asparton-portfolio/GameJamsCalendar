import Jam from "./Jam"

export default function JamsGrid({ jams }) {
  return (
    <ul style={{
      margin: '5em',
      display: 'flex',
      flexFlow: 'row wrap',
      justifyContent: 'space-around',
      alignItems: 'center'
    }}>
      {jams.map(jam =>
        <li key={jam.name} style={{ margin: '2em' }}>
          <Jam jam={jam} />
        </li>
      )}
    </ul>
  )
}
