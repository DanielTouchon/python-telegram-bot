#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2024
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program. If not, see [http://www.gnu.org/licenses/].
"""This module contains objects that represent paid media in Telegram."""

from typing import TYPE_CHECKING, Dict, Final, Optional, Sequence, Tuple, Type

from telegram import constants
from telegram._files.photosize import PhotoSize
from telegram._files.video import Video
from telegram._telegramobject import TelegramObject
from telegram._utils import enum
from telegram._utils.argumentparsing import parse_sequence_arg
from telegram._utils.types import JSONDict

if TYPE_CHECKING:
    from telegram import Bot


class PaidMedia(TelegramObject):
    """Describes the paid media added to a message. Currently, it can be one of:

    * :class:`telegram.PaidMediaPreview`
    * :class:`telegram.PaidMediaPhoto`
    * :class:`telegram.PaidMediaVideo`

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`type` is equal.

    .. versionadded:: NEXT.VERSION

    Args:
        type (:obj:`str`): Type of the paid media.

    Attributes:
        type (:obj:`str`): Type of the paid media.
    """

    __slots__ = ("type",)

    PREVIEW: Final[str] = constants.PaidMediaType.PREVIEW
    """:const:`telegram.constants.PaidMediaType.PREVIEW`"""
    PHOTO: Final[str] = constants.PaidMediaType.PHOTO
    """:const:`telegram.constants.PaidMediaType.PHOTO`"""
    VIDEO: Final[str] = constants.PaidMediaType.VIDEO
    """:const:`telegram.constants.PaidMediaType.VIDEO`"""

    def __init__(
        self,
        type: str,  # pylint: disable=redefined-builtin
        *,
        api_kwargs: Optional[JSONDict] = None,
    ) -> None:
        super().__init__(api_kwargs=api_kwargs)
        self.type: str = enum.get_member(constants.PaidMediaType, type, type)

        self._id_attrs = (self.type,)
        self._freeze()

    @classmethod
    def de_json(
        cls, data: Optional[JSONDict], bot: Optional["Bot"] = None
    ) -> Optional["PaidMedia"]:
        """Converts JSON data to the appropriate :class:`PaidMedia` object, i.e. takes
        care of selecting the correct subclass.

        Args:
            data (Dict[:obj:`str`, ...]): The JSON data.
            bot (:class:`telegram.Bot`, optional): The bot associated with this object.

        Returns:
            The Telegram object.

        """
        data = cls._parse_data(data)

        if data is None:
            return None

        if not data and cls is PaidMedia:
            return None

        _class_mapping: Dict[str, Type[PaidMedia]] = {
            cls.PREVIEW: PaidMediaPreview,
            cls.PHOTO: PaidMediaPhoto,
            cls.VIDEO: PaidMediaVideo,
        }

        if cls is PaidMedia and data.get("type") in _class_mapping:
            return _class_mapping[data.pop("type")].de_json(data=data, bot=bot)

        return super().de_json(data=data, bot=bot)


class PaidMediaPreview(PaidMedia):
    """The paid media isn't available before the payment.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`width`, :attr:`height`, and :attr:`duration`
    are equal.

    .. versionadded:: NEXT.VERSION

    Args:
        type (:obj:`str`): Type of the paid media, always :tg-const:`telegram.PaidMedia.PREVIEW`.
        width (:obj:`int`, optional): Media width as defined by the sender.
        height (:obj:`int`, optional): Media height as defined by the sender.
        duration (:obj:`int`, optional): Duration of the media in seconds as defined by the sender.

    Attributes:
        type (:obj:`str`): Type of the paid media, always :tg-const:`telegram.PaidMedia.PREVIEW`.
        width (:obj:`int`): Optional. Media width as defined by the sender.
        height (:obj:`int`): Optional. Media height as defined by the sender.
        duration (:obj:`int`): Optional. Duration of the media in seconds as defined by the sender.
    """

    __slots__ = ("duration", "height", "width")

    def __init__(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        duration: Optional[int] = None,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ) -> None:
        super().__init__(type=PaidMedia.PREVIEW, api_kwargs=api_kwargs)

        with self._unfrozen():
            self.width: Optional[int] = width
            self.height: Optional[int] = height
            self.duration: Optional[int] = duration

            self._id_attrs = (self.type, self.width, self.height, self.duration)


class PaidMediaPhoto(PaidMedia):
    """
    The paid media is a photo.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`photo` are equal.

    .. versionadded:: NEXT.VERSION

    Args:
        type (:obj:`str`): Type of the paid media, always :tg-const:`telegram.PaidMedia.PHOTO`.
        photo (Sequence[:class:`telegram.PhotoSize`]): The photo.

    Attributes:
        type (:obj:`str`): Type of the paid media, always :tg-const:`telegram.PaidMedia.PHOTO`.
        photo (Tuple[:class:`telegram.PhotoSize`]): The photo.
    """

    __slots__ = ("photo",)

    def __init__(
        self,
        photo: Sequence["PhotoSize"],
        *,
        api_kwargs: Optional[JSONDict] = None,
    ) -> None:
        super().__init__(type=PaidMedia.PHOTO, api_kwargs=api_kwargs)

        with self._unfrozen():
            self.photo: Tuple[PhotoSize, ...] = parse_sequence_arg(photo)

            self._id_attrs = (self.type, self.photo)

    @classmethod
    def de_json(
        cls, data: Optional[JSONDict], bot: Optional["Bot"] = None
    ) -> Optional["PaidMediaPhoto"]:
        data = cls._parse_data(data)

        if not data:
            return None

        data["photo"] = PhotoSize.de_list(data.get("photo"), bot=bot)
        return super().de_json(data=data, bot=bot)  # type: ignore[return-value]


class PaidMediaVideo(PaidMedia):
    """
    The paid media is a video.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`video` are equal.

    .. versionadded:: NEXT.VERSION

    Args:
        type (:obj:`str`): Type of the paid media, always :tg-const:`telegram.PaidMedia.VIDEO`.
        video (:class:`telegram.Video`): The video.

    Attributes:
        type (:obj:`str`): Type of the paid media, always :tg-const:`telegram.PaidMedia.VIDEO`.
        video (:class:`telegram.Video`): The video.
    """

    __slots__ = ("video",)

    def __init__(
        self,
        video: Video,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ) -> None:
        super().__init__(type=PaidMedia.VIDEO, api_kwargs=api_kwargs)

        with self._unfrozen():
            self.video: Video = video

            self._id_attrs = (self.type, self.video)

    @classmethod
    def de_json(
        cls, data: Optional[JSONDict], bot: Optional["Bot"] = None
    ) -> Optional["PaidMediaVideo"]:
        data = cls._parse_data(data)

        if not data:
            return None

        data["video"] = Video.de_json(data.get("video"), bot=bot)
        return super().de_json(data=data, bot=bot)  # type: ignore[return-value]


class PaidMediaInfo(TelegramObject):
    """
    Describes the paid media added to a message.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`star_count` and :attr:`paid_media` are equal.

    .. versionadded:: NEXT.VERSION

    Args:
        star_count (:obj:`int`): The number of Telegram Stars that must be paid to buy access to
            the media.
        paid_media (Sequence[:class:`telegram.PaidMedia`]): Information about the paid media.

    Attributes:
        star_count (:obj:`int`): The number of Telegram Stars that must be paid to buy access to
            the media.
        paid_media (Tuple[:class:`telegram.PaidMedia`]): Information about the paid media.
    """

    __slots__ = ("paid_media", "star_count")

    def __init__(
        self,
        star_count: int,
        paid_media: Sequence[PaidMedia],
        *,
        api_kwargs: Optional[JSONDict] = None,
    ) -> None:
        super().__init__(api_kwargs=api_kwargs)
        self.star_count: int = star_count
        self.paid_media: Tuple[PaidMedia, ...] = parse_sequence_arg(paid_media)

        self._id_attrs = (self.star_count, self.paid_media)
        self._freeze()

    @classmethod
    def de_json(
        cls, data: Optional[JSONDict], bot: Optional["Bot"] = None
    ) -> Optional["PaidMediaInfo"]:
        data = cls._parse_data(data)

        if not data:
            return None

        data["paid_media"] = PaidMedia.de_list(data.get("paid_media"), bot=bot)
        return super().de_json(data=data, bot=bot)
