import PropTypes from 'prop-types';

import { ActionIcon } from '@mantine/core'
import { IconHeartPlus } from '@tabler/icons'

export default function SaveJamButton({ onSaveClick }) {
  return (
    <ActionIcon
      variant='default'
      size='xl'
      radius='md'
      onClick={_e => onSaveClick()}
      style={{
          zIndex: 10,
          position: 'absolute',
          top: 5,
          left: 335
      }}
    >
      <IconHeartPlus size={28} />
    </ActionIcon>
  )
}

SaveJamButton.propTypes = {
    onSaveClick: PropTypes.func
}